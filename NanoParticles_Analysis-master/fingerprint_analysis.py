#!/usr/bin/python3
# author Yates

"""
该文件包含频繁项和指纹提取阶段所有模块：
1. 频繁项提取
2. 不同支持度组合下筛选每种纯样品的特有频繁项（只有纯样品）
3. 指纹分析，即匹配每个指纹包含的颗粒，统计指纹包含颗粒数浓度（热力图文件）
4. 基于2、3，计算该支持度组合下每种纯样品的单位质量颗粒数，并得到该组合下的训练集（只有纯样品）
5. 基于3、4，计算配置样品在选定的纯样品的单位质量颗粒数下的质量分布（只有配置样品）
"""

import os
import re
import shutil
import warnings

import numpy as np
import pandas as pd
from matminer.featurizers.composition import ElementProperty
from mlxtend.frequent_patterns import apriori, association_rules
from pymatgen.core import Composition
from sklearn.ensemble import IsolationForest
from const import isotopes_li
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

warnings.filterwarnings('ignore')


def isotope_to_element(isotope):
    """
    将同位素转化为元素
    :param isotope: 同位素名，如'27Al'
    :return: 元素名，如'Al'
    """
    return re.search('[A-Za-z]+', isotope).group()


def has_isotopes(cali_curve_file):
    """
    根据calibration_curves.csv判断是否有同位素
    """
    cali_curve = read_csv_bigint_embedding(cali_curve_file)
    analyte, slope = cali_curve["analyte"], cali_curve["slope (cps/ppb)"]
    analyte = analyte.str[1:-2].tolist()
    elements = list(map(isotope_to_element, analyte))
    if len(elements) == len(set(elements)):
        return False
    return True


def read_csv_bigint_embedding(file, index_col=None):
    df = pd.read_csv(file, index_col=index_col)
    if "embedding" in df:
        df["embedding"] = df["embedding"].apply(lambda x: int(x))
    return df


class AprioriProcess:
    """
    提取频繁项（纯样品，配置样品，真实样品都需要），并对提取出的频繁项进行压缩，排序处理(按照同位素个数降序排序)
    """

    def __init__(self, substance, min_support=0.1, pure_flag=False, iter_flag=True):
        """
        :param substance: 物质名称，如'meihui','s1'
        :param min_support: 支持度support阈值。非纯样品默认0.01；纯样品可修改，建议 [0.003,0.009]
        :param pure_flag: 要处理的物质是否是纯物质样品，默认False。若是，置为True
        :param iter_flag: 要处理的particle.csv是否是用迭代法得到的，默认True。若是泊松法，置为False
        """
        self.substance = substance
        self.pure_flag = pure_flag
        self.iter_flag = iter_flag
        # self.support = min_support if pure_flag else 0.01  # 纯样品要输入支持度support，非纯样品默认0.01
        self.support = min_support
        self.confidence = 0.2 if pure_flag else 0.3  # 置信度confidence阈值。非纯样品默认0.3，纯样品默认0.2
        self.max_len = 4  # 频繁项中包含同位素的最大个数，默认4
        self.lift = 1.2  # 相关性lift阈值,默认1.2
        self.df = None  # particle.csv文件
        self.iso_emb = None  # 同位素的embedding
        self.dir_name = '_'.join([substance, 'iteration']) if iter_flag else '_'.join([substance, 'poisson'])
        self.unknown_detect = False

    def update_files(self):
        """
        读取并更新self.df, self.iso_emb
        :return:
        """
        print(self.dir_name)
        if not os.path.exists(self.dir_name):  # 目录不正确
            return self.dir_name + " not exist!"

        else:  # 目录正确，读取'particle.csv'文件和'isotopes.info.csv'文件
            data_csv = 'particle.csv'
            try:
                self.df = read_csv_bigint_embedding('/'.join([self.dir_name, data_csv]))
            except (TypeError, FileNotFoundError):
                return '/'.join([self.dir_name, data_csv]) + " not exist!"

            iso_info = 'isotopes_info.csv'
            try:
                self.iso_emb = read_csv_bigint_embedding(iso_info, index_col=0)['embedding']
            except (TypeError, FileNotFoundError):
                return "isotopes_info.csv not exist!"

    def apriori(self):
        """
        Apriori算法提取频繁项，返回频繁项信息df
        :return: 频繁项信息df
        """
        # self.update_files()
        file_state = self.update_files()
        if file_state is not None:
            return file_state
        bool_df = self.df.iloc[:, :-1].notnull()

        # 求频繁项集：导入apriori方法设置最小支持度min_support求频繁项集合，同时最大长度不超过max_len。
        frequent_itemsets = apriori(bool_df, min_support=self.support, max_len=self.max_len, use_colnames=True)

        # 求关联规则：导入association_rules方法引入关联规则min_confidence。
        association_rule = association_rules(frequent_itemsets, metric='confidence',
                                             min_threshold=self.confidence).iloc[:, 0:-2]
        association_rule = association_rule[association_rule['lift'] > self.lift].iloc[:, [0, 1, 4]]
        return association_rule

    def apriori_del_repeat(self):
        """
        对Apriori算法得到结果中的重复项进行压缩。
        :return: 返回压缩重复项后的df
        """
        association_rule_df = self.apriori()
        if isinstance(association_rule_df, str):
            return association_rule_df
        new_df = association_rule_df.iloc[0].to_frame().T
        iso_set = set()
        tmp_set = set()
        [iso_set.add(item) for s in association_rule_df.iloc[0, 0:2] for item in s]

        for r in range(association_rule_df.shape[0]):
            tmp_set.clear()
            for s in association_rule_df.iloc[r, 0:2]:
                for item in s:
                    tmp_set.add(item)
            if tmp_set != iso_set:
                iso_set.clear()
                [iso_set.add(item) for item in tmp_set]
                new_df = new_df.append(association_rule_df.iloc[r])
        new_df = new_df.reset_index(drop=True)
        return new_df

    def apriori_final(self):
        """
        将去重后的frozenset合并，统计每个集合的长度，按照长度降序排序，并将最终结果保存为csv。
        :return: 去重并排序后的频繁项df
        """
        association_compressed = self.apriori_del_repeat()
        if isinstance(association_compressed, str):
            return association_compressed
        support = association_compressed.iloc[:, -1].values
        new_set_li = list()
        len_set_li = list()
        bin_emb_li = list()

        def merge_frozenset(row):
            """
            将两个frozenset合并为一个set
            :param row: 行
            :return:
            """
            new_set = set(row[0].union(row[1]))
            new_set_li.append(new_set)
            len_set_li.append(len(new_set))
            emb_tmp = 0
            for e in new_set:
                emb_tmp += self.iso_emb[e]
            bin_emb_li.append(emb_tmp)

        association_compressed.apply(lambda x: merge_frozenset(x), axis=1)
        association_final = pd.DataFrame([new_set_li, bin_emb_li, len_set_li, support], index=None).T
        association_final.columns = ['FrequentItem', 'embedding', 'iso_num', 'support']
        association_final = association_final.sort_values(by='iso_num', ascending=False)
        filename = ''.join(['support_', str(self.support)[:5], '.csv'])
        print("support file")
        association_final.to_csv('/'.join([self.dir_name, filename]), index=None)
        print(f"When support equals {self.support}, the total count of frequent items is {association_final.shape[0]}.")


class FIAnalysis:
    """
    真实/配置样品查找频繁项对应的颗粒，并统计每个频繁项对应的颗粒数。生成该物质的测试集文件以及热力图文件。
    """

    def __init__(self, substance, support, iter_flag=True):
        """
        :param substance: 样品名，如：'s1'
        :param iter_flag: 要处理的particle.csv是否是用迭代法得到的，默认True。若是泊松法，置为False
        """
        self.substance = substance
        self.iter_flag = iter_flag
        self.support = support
        self.df = None
        self.fi_df = None
        self.dir_name = ''
        self.fi_ana = None
        self.udetect = True

    def update_files(self):
        """
        拼接该物质文件所在的文件夹路径，并读取particle并更新self.df；读取support_0.01.csv并更新self.fi_df
        :return:
        """
        suffix = 'iteration' if self.iter_flag else 'poisson'
        self.dir_name = '_'.join([self.substance, suffix])

        if not os.path.exists(self.dir_name):  # 目录不正确
            return self.dir_name + ' not exist!'

        else:  # 目录正确，切换到目录下并读取'particle.csv'文件
            particle_file = 'particle.csv'
            try:
                self.df = read_csv_bigint_embedding('/'.join([self.dir_name, particle_file]))
            except (TypeError, FileNotFoundError):
                return '/'.join([self.dir_name, particle_file]) + ' not exist!'

            fi_file = 'support_' + str(self.support)[:5] + '.csv'
            try:
                self.fi_df = read_csv_bigint_embedding('/'.join([self.dir_name, fi_file]))
            except (TypeError, FileNotFoundError):
                return '/'.join([self.dir_name, fi_file]) + ' not exist!'

    # def isotope_to_element(self, isotope):
    #     """
    #     将同位素转化为元素
    #     :param isotope: 同位素名，如'27Al'
    #     :return: 元素名，如'Al'
    #     """
    #     return re.search('[A-Za-z]+', isotope).group()

    def columns_to_elements(self):
        """
        将self.df的columns转成元素表示并更新self.df
        :return:
        """
        col = self.df.columns
        iso_li = col[:-1]
        emb = col[-1]
        # new_col = list(map(self.isotope_to_element, iso_li))
        new_col = list(iso_li)
        print(new_col)
        new_col.append(emb)
        self.df.columns = new_col

    def frequentitem_to_elements(self, fi):
        """
        将FrequentItem中的同位素集合 {iso1,iso2,..} 转成 ele1-ele2-...的元素组合形式。
        :param fi: 频繁项的集合表示
        :return:
        """
        fi = list(eval(fi))
        # print(fi)
        # ele_comp = re.search('[A-Za-z]+', fi[0]).group()
        ele_comp = fi[0]
        for iso in fi[1:]:
            # ele = re.search('[A-Za-z]+', iso).group()
            ele = iso
            ele_comp = '-'.join([ele_comp, ele])
        return ele_comp

    def get_percentage(self, row):
        """
        将数量分布转为数量比分布
        :param row: 数量分布
        :return: 数量比分布
        """
        total = row.sum()
        percent = row / total
        percent[percent < 1e-3] = 0.0
        return percent

    def get_comps(self, row):
        """
        根据频繁项(指纹)的元素分布，得到频繁项(指纹)的化学式
        :param row: 频繁项(指纹)的元素分布
        :return: 该频繁项(指纹)的化学式
        """
        return Composition(''.join([isotope_to_element(i[0]) + str(i[1]) for i in list(row.to_dict().items())]))

    def isolation_forest(self, data):
        """
        使用孤立森林的算法，检测异常点
        :data: 包含频繁项信息(每种元素出现的次数，元素组成，embedding，包含元素个数，包含的颗粒数)的df
        :return: 该频繁项(指纹)的化学式
        """
        rng = np.random.RandomState(42)
        n_samples = len(data)
        outliers_fraction = 0.05
        data_train = data
        clf = IsolationForest(max_samples=n_samples, random_state=rng, contamination=outliers_fraction)
        clf.fit(data)
        data_pred = clf.predict(data_train)
        return data_pred

    def unknown_detect(self, data):
        """
        规范数据的格式，之后调用孤立森林的算法
        :data: 包含频繁项信息(每种元素出现的次数，元素组成，embedding，包含元素个数，包含的颗粒数)的df
        :return: 每个样品的未知源标签
        """
        # 调用magpie预处理
        elem_col = [col for col in data.columns if col in isotopes_li]
        data[elem_col] = data[elem_col].apply(lambda x: self.get_percentage(x), axis=1)
        data['formula'] = data[elem_col].apply(self.get_comps, axis=1)
        ep = ElementProperty.from_preset(preset_name='magpie')
        # ep.features = ['Number']
        data = ep.featurize_dataframe(data[['formula']], 'formula').drop('formula', axis=1).values

        label = self.isolation_forest(data)
        return label

    def fi_analysis(self, TE, V, T, Vf, m, Df, ud=True):
        """
        查询每个频繁项包含的颗粒后统计每个频繁项的信息，更新self.fi_ana。
        通过ud参数选择是否需要进行未知源的检测。unknown_detect的默认值为true
        :return: 包含频繁项信息(每种元素出现的次数，元素组成，embedding，包含元素个数，包含的颗粒数，是否为未知源(取决于ud的值))的df
        """
        file_state = self.update_files()
        if isinstance(file_state, str):
            return file_state
        self.columns_to_elements()
        data_idx = set(self.df.index)
        data_emb = self.df['embedding'].values
        for i in range(len(self.fi_df)):
            iso = self.fi_df.iloc[i, 0]
            emb = self.fi_df.iloc[i, 1]
            iso_n = self.fi_df.iloc[i, 2]
            row_idx = np.squeeze(np.argwhere(emb == data_emb & emb))
            row_idx = list(set(row_idx) & data_idx)
            if len(row_idx) == 0:
                continue
            data_idx -= set(row_idx)
            tmp_df = self.df.iloc[row_idx]
            fi_ana = tmp_df.iloc[:, 0:-1].count().to_frame().T  # 若要得到每个频繁项包含的颗粒，从此处开始修改。
            fi_ana['component'] = self.frequentitem_to_elements(iso)
            fi_ana['number'] = len(row_idx)
            fi_ana['PNC'] = len(row_idx)
            fi_ana['length'] = int(iso_n)
            fi_ana['embedding'] = int(emb)
            self.fi_ana = pd.concat([self.fi_ana, fi_ana])

        elem_col = [col for col in self.fi_ana.columns if col in isotopes_li] + ["PNC"]

        if ud:
            data_copy = pd.DataFrame(self.fi_ana)  # 保留转换为百分比前的数据
            detect_result = self.unknown_detect(data=self.fi_ana)
            self.fi_ana[elem_col] = data_copy[elem_col]  # 恢复转换为百分比前的数据
            substance_data = []
            for i in range(len(detect_result)):
                if detect_result[i] == -1:
                    substance_data.append('unknown')
                else:
                    substance_data.append('')
            self.fi_ana.insert(self.fi_ana.shape[1] - 2, 'substance', substance_data)
            self.fi_ana = self.fi_ana.drop('formula', axis=1)

        self.fi_ana[elem_col] = self.fi_ana[elem_col] * Df * 60 * Vf / (TE * V * T * m)
        # self.fi_ana["PNC"] = self.fi_ana["PNC"].apply(lambda x: x * Df * 60 * Vf / (TE * V * T * m))

        self.fi_ana = self.fi_ana.reset_index(drop=True)
        print("test file")
        path = '/'.join([self.dir_name, 'test_' + str(self.support)[:5] + '.csv'])
        if os.path.exists('/'.join(['sample', path])):
            os.remove('/'.join(['sample', path]))
        self.fi_ana.to_csv(path, index=None)


class HeatMapGenerator:
    def __init__(self, substance, support, iter_flag=True):
        """
        :param substance: 样品名，如：'s1'
        :param iter_flag: 要处理的particle.csv是否是用迭代法得到的，默认True。若是泊松法，置为False
        """
        self.substance = substance
        self.iter_flag = iter_flag
        self.support = support
        self.dir_name = ''
        self.fi_ana = None

    def update_files(self):
        """
        拼接该物质文件所在的文件夹路径，并读取particle并更新self.df；读取support_0.01.csv并更新self.fi_df
        :return:
        """
        suffix = 'iteration' if self.iter_flag else 'poisson'
        self.dir_name = '_'.join([self.substance, suffix])

        if not os.path.exists(self.dir_name):  # 目录不正确
            return self.dir_name + ' not exist!'

        else:  # 目录正确，切换到目录下并读取'test_xxx.csv'文件
            test_file = 'test_' + str(self.support)[:5] + '.csv'
            try:
                self.fi_ana = read_csv_bigint_embedding('/'.join([self.dir_name, test_file]))
            except (TypeError, FileNotFoundError):
                return '/'.join([self.dir_name, test_file]) + ' not exist!'

    def heat_map_file(self, base, V, T, Vi=0.05):
        """
        生成并保存绘制热力图的文件。
        :param base: log的底数
        :param V: 流速(ml/min)
        :param Vi: 进样体积，默认0.05
        :param T: 测试时间(s)
        :return:
        """
        file_state = self.update_files()
        if isinstance(file_state, str):
            return file_state
        comp = self.fi_ana[['component']]

        target_cols = [col for col in self.fi_ana.columns if col in isotopes_li]
        eles = self.fi_ana[target_cols].apply(lambda x: x * (V * T) / (Vi * 60)).replace(0, 1)

        eles = np.log(eles) / np.log(base)
        hm_df = pd.concat([comp, eles], axis=1)
        path = ''.join(
            [self.dir_name, '/HeatMap_', 'base=', str(base), '_support=', str(self.support)[:5],
             '.csv'])
        hm_df.to_csv(path, index=False)
        print("heatmap file")
        print(f'Frequent items\' analysis (test set file and heat map file) has been finished, '
              f'which includes {hm_df.shape[0]} frequent items.')


class FingerprintExtract:
    """
    将一批数据中所有纯样品的频繁项embedding表示合成一个列表，并对其使用TF-IDF算法提取每种物质的指纹（特有成分）。
    """

    def __init__(self, substance_support_dic, number):
        """
        :param substance_support_dic: 所有纯样品文件夹名称和该种纯样品支持度的字典（字典按照纯样品入库时顺序）
        :param number: 纯样品数量
        """
        self.substance_support_dic = substance_support_dic
        self.number = number
        self.iso_emb = None  # 同位素的embedding
        self.group_dir = ''  # 分组的目录名

        # 字典长度不等于number
        if len(self.substance_support_dic) != self.number:
            raise Exception(f'The number of pure substance is wrong!')

    def group_mkdir(self):
        """
        创建support组合对应分组的文件夹
        纯样品的support一般在 [0.003, 0.009]，选取间隔为0.001，因此将support最后两位数字作为该种纯样品的supprot索引
        :return:
        """
        for val in self.substance_support_dic.values():
            param = str(val)[-3:]
            self.group_dir = ''.join([self.group_dir, param])
        if os.path.exists(self.group_dir):
            shutil.rmtree(self.group_dir)
        os.mkdir(self.group_dir)
        print(f'The group directory {self.group_dir} has been create!')

    def get_sup_df(self, dir_name, support):
        """
        得到某种物质support_x.csv的路径，并读取得该文件对应的df。并把该物质的particle.csv文件复制到该文件夹下
        :param dir_name: 该种纯样品的目录名
        :param support: 该种纯样品要使用的support_x.csv文件
        :return: 该文件对应的df
        """
        sup_file = ''.join(['support_', str(support), '.csv'])
        sup_path = '/'.join([dir_name, sup_file])
        try:
            sup_df = read_csv_bigint_embedding(sup_path)
        except (TypeError, FileNotFoundError):
            return sup_path + " not exist!"
        shutil.copy('/'.join([dir_name, 'particle.csv']),
                    ''.join([self.group_dir, '/', 'particle_', dir_name.split('_')[0], '.csv']))
        return sup_df

    def get_iso_emb(self):
        """
        读取同位素embeddings
        :return:
        """
        iso_info = 'isotopes_info.csv'
        try:
            self.iso_emb = read_csv_bigint_embedding(iso_info, index_col=0)['embedding']
        except (TypeError, FileNotFoundError):
            return "isotopes_info.csv not exist!"

    def decode_embedding(self, embedding):
        """
        对embedding解码，得到同位素组合(按原子质量升序排列)。
        :param embedding: 指纹的embeddding
        :return: 指纹的同位素组合
        """
        iso_emb = self.iso_emb
        iso_li = list()
        for i in range(len(iso_emb)):
            if iso_emb[i] == embedding & iso_emb[i]:
                iso_li.append(iso_emb.index[i])
        return iso_li

    def merge_embedding(self):
        """
        将每种纯样品的所有频繁项embedding合成一个空格分隔的字符串，并将所有纯样品的embedding字符串合成一个列表。
        :return: 所有纯样品的embedding字符串合成的列表
        """
        all_emb = list()  # 所有物质的频繁项二进制编码(以空格分隔)字符串组成的列表
        for sub_dir, sup in self.substance_support_dic.items():
            sup_df = self.get_sup_df(sub_dir, sup)
            if isinstance(sup_df, str):
                return sup_df
            emb = sup_df['embedding']
            emb_str = list(map(str, emb))
            all_emb.append(' '.join(emb_str))
        return all_emb

    def compute_tfidf(self):
        """
        对所有纯样品选中的的频繁项文件中的embedding组成的数据进行TFIDF计算,得到对应的weights数组。
        :return: TFIDF权重矩阵
        """
        all_emb = self.merge_embedding()
        if isinstance(all_emb, str):
            return all_emb
        vectorizer = CountVectorizer()  # CountVectorizer:将文本中的词语转换为词频矩阵
        X = vectorizer.fit_transform(all_emb)  # 计算每个频繁项出现的次数(频率)
        keywords = vectorizer.get_feature_names()  # 获取数据集中所有出现的频繁项(关键词)。查看X的值:X.toarray()

        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(X)  # 将频率矩阵X统计成TF-IDF值
        weights = tfidf.toarray()  # tfidf[i][j]表示i类物质中的第j个成分的tfidf值

        return weights, keywords

    def get_fingerprints(self):
        """
        从tfidf得到的weights中选出每种纯物质tfidf值最高的频繁项（即指纹），并对其进行解码。
        :return: 保存包括[同位素组成、embedding、同位素数量]的指纹csv。
        """
        iso_file = self.get_iso_emb()
        if isinstance(iso_file, str):
            return iso_file
        self.group_mkdir()
        weight_matrix = self.compute_tfidf()
        if isinstance(weight_matrix, str):
            return weight_matrix
        weights, keywords = weight_matrix
        # weights, keywords = self.compute_tfidf()
        cols = ['FingerPrint', 'embedding']
        substance_li = list(self.substance_support_dic.keys())
        for i in range(len(weights)):
            substance = substance_li[i]  # 该种物质的名称
            weight = weights[i]
            emb_res = list()  # 特有成分的emb
            iso_res = list()  # 特有成分的同位素组成
            max_val = max(weight)  # 该种物质的最大tfidf值，即特有成分的tfidf值

            for j in range(len(weight)):
                if weight[j] == max_val:
                    embedding = int(keywords[j])
                    isotopes = self.decode_embedding(embedding)
                    emb_res.append(embedding)
                    iso_res.append(isotopes)

            file_name = ''.join(['fp_', substance.split('_')[0], '.csv'])
            path = '/'.join([self.group_dir, file_name])
            fp_df = pd.DataFrame(np.array([iso_res, emb_res], dtype=object).T, columns=cols)
            fp_df['iso_num'] = [len(iso) for iso in fp_df['FingerPrint']]
            fp_df = fp_df.sort_values(by='iso_num', ascending=False)
            fp_df.to_csv(path, index=None)
            print(f'{substance}\' s finger prints have been extracted.')
        print('-' * 50)


class FPAnalysis:
    """
    纯样品查找频繁项对应的颗粒，并统计每个频繁项对应的颗粒数。生成该分组的训练集文件以及每种纯样品的热力图文件。
    """

    def __init__(self, group, substance_li):
        """
        :param group: 分组目录名，如’006005008‘
        :param substance_li: 纯样品名称列表
        """
        self.group = group
        self.substance_li = substance_li
        self.df = None  # particle文件df
        self.fp_df = None  # fp文件df
        self.train_set = None
        self.mass_density = dict()  # 每种物质包含的颗粒总数，计算单位质量颗粒数要用到

    def update_files(self, sub):
        """
        读取一种纯样品的particle和fp文件，并更新self.df, self.fp_df
        :param sub: 物质名
        :return:
        """
        ptc_file = ''.join(['particle_', sub, '.csv'])
        ptc_path = '/'.join([self.group, ptc_file])
        print(ptc_path)
        try:
            self.df = read_csv_bigint_embedding(ptc_path)
        except (TypeError, FileNotFoundError):
            return ptc_path + " not exist!"
        fp_file = ''.join(['fp_', sub, '.csv'])
        fp_path = '/'.join([self.group, fp_file])
        try:
            self.fp_df = read_csv_bigint_embedding(fp_path)
        except (TypeError, FileNotFoundError):
            return fp_path + " not exist!"

    # def isotope_to_element(self, isotope):
    #     """
    #     将同位素转化为元素
    #     :param isotope: 同位素名，如'27Al'
    #     :return: 元素名，如'Al'
    #     """
    #     return re.search('[A-Za-z]+', isotope).group()

    def columns_to_elements(self):
        """
        将self.df的columns转成元素表示并更新self.df
        :return:
        """
        col = self.df.columns
        iso_li = col[:-1]
        emb = col[-1]
        # new_col = list(map(self.isotope_to_element, iso_li))
        new_col = list(iso_li)
        new_col.append(emb)
        self.df.columns = new_col

    def fingerprint_to_elements(self, fp):
        """
        将FingerPrint中的同位素集合 {iso1,iso2,..} 转成 ele1-ele2-...的元素组合形式。
        :param fp: 频繁项的集合表示
        :return:
        """
        fp = list(eval(fp))
        # ele_comp = re.search('[A-Za-z]+', fp[0]).group()
        ele_comp = fp[0]
        for iso in fp[1:]:
            # ele = re.search('[A-Za-z]+', iso).group()
            ele = iso
            ele_comp = '-'.join([ele_comp, ele])
        return ele_comp

    def fp_analysis(self, TE, V, T, Df_list, Vf_list, m_list):
        """
        查询每个指纹包含的颗粒后统计每个频繁项的信息，将所有纯样品指纹的信息拼接作为该分组下的训练集。
        :return: 包含频繁项信息(每种元素出现的次数，元素组成，embedding，包含元素个数，包含的颗粒数)的测试集
        """
        for k, sub in enumerate(self.substance_li):
            Df = Df_list[k]
            Vf = Vf_list[k]
            m = m_list[k]
            file_state = self.update_files(sub)
            if isinstance(file_state, str):
                return file_state
            self.columns_to_elements()
            data_idx = set(self.df.index)
            data_emb = self.df['embedding'].values
            sub_train_set = None
            for i in range(len(self.fp_df)):
                iso = self.fp_df.iloc[i, 0]
                emb = self.fp_df.iloc[i, 1]
                iso_n = self.fp_df.iloc[i, 2]
                row_idx = np.squeeze(np.argwhere(emb == data_emb & emb))
                row_idx = list(set(row_idx) & data_idx)
                if len(row_idx) == 0:
                    continue
                data_idx -= set(row_idx)
                tmp_df = self.df.iloc[row_idx]
                fp_ana = tmp_df.iloc[:, 0:-1].count().to_frame().T  # 若要得到每个频繁项包含的颗粒，从此处开始修改。
                fp_ana = fp_ana * Df * 60 * Vf / (TE * V * T * m)

                fp_ana['component'] = self.fingerprint_to_elements(iso)
                fp_ana['number'] = len(row_idx)
                fp_ana['PNC'] = len(row_idx) * Df * 60 * Vf / (TE * V * T * m)
                fp_ana['length'] = int(iso_n)
                fp_ana['embedding'] = int(emb)

                sub_train_set = pd.concat([sub_train_set, fp_ana])
            sub_train_set['substance'] = sub
            self.mass_density[sub] = sub_train_set['number'].sum()
            self.train_set = pd.concat([self.train_set, sub_train_set])
        self.train_set = self.train_set.reset_index(drop=True)
        path = '/'.join([self.group, 'train.csv'])
        self.train_set.to_csv(path, index=False)

    def heat_map_file(self, base, V, T, Vi):
        """
        对每种纯样品，生成并保存绘制热力图的文件。
        :param base: log的底数
        :param V: 流速(ml/min)
        :param Vi: 进样体积，默认0.05
        :param T: 测试时间(s)
        :return:
        """
        for sub in self.substance_li:
            # coef = Vf * Df / (TE * Vi * m)
            sub_df = self.train_set.groupby('substance').get_group(sub)
            comp = sub_df[['component']]

            target_cols = [col for col in sub_df.columns if col in isotopes_li]

            eles = sub_df[target_cols].apply(lambda x: x * (V * T) / (Vi * 60)).replace(0, 1)
            eles = np.log(eles) / np.log(base)
            hm_df = pd.concat([comp, eles], axis=1)
            path = ''.join([self.group, '/HeatMap_', sub, '.csv'])
            hm_df.to_csv(path, index=False)
        print(f'Finger print\' analysis (train set file and heat map files) has been finished.')

    def get_mass_density(self, mass_list):
        """
        得到该分组下纯样品的单位质量颗粒数，并保存为csv，支持多个纯样品不同质量
        :param mass_list: 纯样品质量列表
        :return:
        """
        # for mass in mass_list:
        mass_density = pd.Series(self.mass_density).to_frame().T
        mass_density.iloc[0] = mass_density.iloc[0] / mass_list
        mass_density.index = [self.group]
        path = ''.join([self.group, '/mass_density.csv'])
        mass_density.to_csv(path)
        print(f'Particle number per gram (mass density) has been computed.')
        return mass_density

    def read_configuration_mass(self):
        """
        读取配置样品的质量文件，并返回df
        :return: 配置样品质量df
        """
        try:
            res = read_csv_bigint_embedding('configuration_samples_mass.csv', index_col=0)
        except (TypeError, FileNotFoundError):
            return "configuration_samples_mass.csv not exist!"
        return res

    def configuration_samples_label(self):
        """
        根据该分组下纯样品的单位质量颗粒数和配置样品中各种物质的质量，计算该分组下配置样品的数量分布(即标签)并保存
        :return:
        """
        config_samples_mass = self.read_configuration_mass()
        if isinstance(config_samples_mass, str):
            return config_samples_mass
        config_samples_number = config_samples_mass * self.mass_density

        def get_number_percentage(row):
            """
            将配置样品颗粒数转为颗粒数量比
            :return: row
            """
            total = row.sum()
            return row / total

        config_samples_number = config_samples_number.apply(lambda x: get_number_percentage(x), axis=1)
        path = ''.join([self.group, '/configuration_samples_label.csv'])
        config_samples_number.to_csv(path)
        print(f'Configuration samples \'s label (particle number percentage in a specific combination of support) '
              f'have been computed.')
