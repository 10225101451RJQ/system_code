#!/usr/bin/python3
# author Yates

"""
该文件包含颗粒态粒子筛选阶段所有模块：
1.颗粒态粒子筛选（泊松法、分类法）
2.计算传输效率TE（标准样品）
3.计算颗粒数浓度（真实样品、纯样品、配置样品）
"""

import os
import re
import warnings
import math

import numpy as np
import pandas as pd

import csv

warnings.filterwarnings('ignore')

""""
origin_filename用于保存文件名，方便之后使用，如s1.csv
"""
origin_filename = ''


def read_csv_bigint_embedding(file, index_col=None):
    df = pd.read_csv(file, index_col=index_col)
    if "embedding" in df:
        df["embedding"] = df["embedding"].apply(lambda x: int(x))
    return df


def get_mass_factor(cali_curve_file, mass_factor_file):
    """
    根据calibration_curves.csv生成mass_factor.csv
    """
    cali_curve = read_csv_bigint_embedding(cali_curve_file)
    analyte, slope = cali_curve["analyte"], cali_curve["slope (cps/ppb)"]
    analyte = analyte.str[1:-2].tolist()
    mass_factor = pd.DataFrame(slope.to_frame().T)
    mass_factor.columns = analyte
    mass_factor.to_csv(mass_factor_file, index=False)


def get_isotopes_info(mass_factor_file):
    """
    读取同位素单位强度文件，并生成同位素embedding，将同位素的单位强度和embedding存在一个csv文件中。
    注：同位素文件中的同位素按照元素周期表顺序升序排。该文件应为csv，放在当前目录下
    :param mass_factor_file: 同位素文件名
    :return:
    """
    file_name = 'isotopes_info.csv'
    if not os.path.exists(file_name):
        iso_df = read_csv_bigint_embedding(mass_factor_file).T
        iso_emb = list()
        for i, iso in enumerate(iso_df.index):
            iso_emb.append(1 << i)
        iso_emb = pd.DataFrame(np.array(iso_emb), index=iso_df.index)
        iso_df = pd.concat([iso_df, iso_emb], axis=1)
        iso_df.columns = ['mass_factor', 'embedding']
        iso_df.to_csv(file_name)
        print("Isotopes' information has been extracted.")
    return file_name


def get_TE(ptc_df, C=1e9, V=0.02, T=150):
    """
    根据标准物质的分类结果计算TE
    :param ptc_df:标准物质颗粒态粒子的df
    :param C: 数浓度(个/ml)
    :param V: 流速(ml/min)
    :param T: 测试时间(s)
    :return: TE值
    """
    file_name = "TE.csv"
    ptc_cnt = ptc_df.count()
    coef = 6e4 / (C * 1000 * V * T)
    TE = pd.DataFrame(ptc_cnt * coef, columns=['197Au'])
    print(TE)
    TE.to_csv(file_name, index=None)
    print("TE have been computed.")
    return TE


class DataLoader:
    """
    筛选颗粒态粒子前对原始数据预处理
    """

    def __init__(self, ori_file_name, iso_file_name):
        """
        :param ori_file_name: 原始数据文件的文件名。(原始数据文件放在当前目录下即可)
        :param iso_file_name:同位素信息csv文件名。(该文件放在当前目录下即可)
        """
        global origin_filename
        origin_filename = ori_file_name
        self.ori_df = read_csv_bigint_embedding(ori_file_name).iloc[:, 2:]
        self.iso_info = read_csv_bigint_embedding(''.join(['../', iso_file_name]), index_col=0)
        self.iso_li = self.iso_info.index.tolist()  # 要研究的同位素列表

    def update_ori_df(self):
        """
        更新ori_df:即在原始文件中选择要研究的同位素
        :return:
        """
        self.ori_df.columns = list(map(lambda x: x[1:-8], self.ori_df.columns.tolist()))
        self.ori_df = self.ori_df[self.iso_li] if self.ori_df.shape[1] > 1 else self.ori_df

    def get_cleaned_data(self):
        """
        清洗数据，将负值置为0
        :return:  返回清洗后数据的df
        """
        self.update_ori_df()
        cleaned_df = self.ori_df
        cleaned_df[cleaned_df < 0] = 0  # 小于0的区域全部置为nan
        return cleaned_df

    def get_basic_metirc(self, cleaned_df):
        """
        得到由 [同位素名称，同位素出现次数，最小强度，最大强度，平均强度，总强度，强度标准差] 6行组成的df，
        并插入metirc列作为index
        :param cleaned_df: self.get_cleaned_data 方法得到的清洗后数据的df
        :return: 同位素层面上述7种指标的df
        """
        count = cleaned_df[cleaned_df > 0].count().to_frame().T  # 某种粒子出现次数
        min_ints = cleaned_df.min().to_frame().T  # 某种粒子强度最小值
        max_ints = cleaned_df.max().to_frame().T  # 某种粒子强度最大值
        sum_ints = pd.DataFrame(np.nansum(cleaned_df, axis=0).reshape(1, -1), columns=self.ori_df.columns)  # 某种粒子强度和
        avg_ints = pd.DataFrame(np.nanmean(cleaned_df, axis=0).reshape(1, -1), columns=self.ori_df.columns)  # 某种粒子强度平均
        std_ints = pd.DataFrame(np.nanstd(cleaned_df, axis=0).reshape(1, -1), columns=self.ori_df.columns)  # 某种粒子强度的标准差
        basic_metric = pd.concat([min_ints, max_ints, count, sum_ints, avg_ints, std_ints], axis=0)
        basic_metric.index = ['min_ints', 'max_ints', 'count', 'sum_ints', 'avg_ints', 'std_ints']
        return basic_metric


class IterMethod:
    """
    迭代分类法分类法筛选颗粒态粒子
    """

    def __init__(self, data_df, metric_df):
        """
        :param data_df: DataLoader中get_cleaned_data方法返回的清洗后数据的df
        :param metric_df: DataLoader中get_basic_metirc返回的同位素统计指标的df
        """
        self.data_df = data_df
        self.metric_df = metric_df
        self.col_name = self.data_df.columns
        self.cur_df = self.data_df  # 每次要被迭代的df
        self.iter_cnt = 0  # 迭代次数
        self.thr = []  #阈值

    def get_avg(self):
        """
        计算每种同位素强度的平均值
        :return: 同位素强度的平均值的np.array
        """
        return np.nanmean(self.cur_df, axis=0)

    def get_std(self):
        """
        计算每种同位素强度的标准差
        :return: 同位素强度的标准差的np.array
        """
        return np.nanstd(self.cur_df, axis=0)

    def get_thr(self):
        """
        求出每个csv文件的阈值并返回对应df,并更新self.iter_cnt。
        计算质量检测限，并存储成文件
        :return: 迭代后同位素强度均值的df
        """
        avg_tmp = self.get_avg()
        std_tmp = self.get_std()
        thr = 3.29 * std_tmp + 2.71 + avg_tmp
        self.thr = thr
        # print(thr)
        thr_df = pd.DataFrame([thr] * len(self.data_df), columns=self.col_name).fillna(0)
        self.iter_cnt += 1
        return thr_df

    def gt_file(self, cnt):
        """
        创建gt文件夹并返回对应迭代轮数的csv文件名。gt目录下是大于强度均值的迭代结果
        :param cnt: 迭代次数
        :return:
        """
        dir_path = os.path.join(os.getcwd(), "gt")
        flag = os.path.exists(dir_path)
        if not flag:
            os.makedirs(dir_path)
        file_name = str(cnt) + ".csv"
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def lt_file(self, cnt):
        """
        创建lt文件夹并返回对应迭代轮数的csv文件名。lt目录下是小于强度均值的迭代结果
        :param cnt: 迭代次数
        :return:
        """
        dir_path = os.path.join(os.getcwd(), "lt")
        flag = os.path.exists(dir_path)
        if not flag:
            os.makedirs(dir_path)
        file_name = str(cnt) + ".csv"
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def update_df(self, thr, cnt):
        """
        根据阈值保存为两个csv文件：'gt/1.csv'、'lt/1.csv'；并返回小于阈值的df
        :param thr: 强度均值
        :param cnt: 迭代次数
        :return:
        """
        gt_df = self.cur_df[self.cur_df >= thr]
        gt_df.to_csv(self.gt_file(cnt), index=None)
        lt_df = self.cur_df[self.cur_df < thr]
        lt_df.to_csv(self.lt_file(cnt), index=None)
        return lt_df

    def iterator(self):
        """
        进行迭代过程
        :return:
        """
        end_DF = self.cur_df
        flag = False
        while not flag:
            beg_DF = end_DF
            THR = self.get_thr()  # self.iter_cnt 在此处已+1
            end_DF = self.update_df(THR, self.iter_cnt)
            self.cur_df = end_DF
            if beg_DF.equals(end_DF):
                flag = True
                print("Iteration have been finished, cnt: %s." % self.iter_cnt)

    def get_final_result(self):
        """
        根据溶解态的结果，得到颗粒态的最终结果并保存。
        :return: 颗粒态粒子的df，溶解态粒子的df, 斜率thr方便后续计算
        """
        res_df = read_csv_bigint_embedding('./lt/' + str(self.iter_cnt) + '.csv')
        # print(f'iter_cnt:{self.iter_cnt}')
        ptc_df = self.data_df[pd.isnull(res_df)]
        # pd.isnull(resolve_df_：溶解态df的非空位为False，空位为True，与清洗后的原始数据做mask得到颗粒态df
        ptc_df.to_csv('./gt/' + str(self.iter_cnt + 1) + '.csv', index=None)
        thr = self.thr
        return ptc_df, res_df, thr


class PoissonMethod:
    """
    泊松分类法筛选颗粒态粒子
    """

    def __init__(self, data_df, metric_df, credible):
        """
        :param data_df: DataLoader中get_cleaned_data方法返回的清洗后数据的df
        :param metric_df: DataLoader中get_basic_metirc返回的同位素统计指标的df
        :param credible: 泊松分布的置信度。(0,1)之间小数，一般选0.997
        """
        self.data_df = data_df
        self.metric_df = metric_df
        self.col_name = self.data_df.columns.tolist()
        self.m = self.metric_df.loc['avg_ints']  # 未归一化的同位素平均强度，归一化处理后作为λ
        self.credible = credible

    def normal_lambda(self):
        """
        将强度均值归一化，得到可用于泊松计算λ。
        λ是归一化后的同位素强度均值，是一个(0,100]的整数
        返回的df包括每种粒子的 [强度均值，λ，scale], 并返回该df，每行都是float。
        :return: [强度均值，λ，scale] 3行组成的df
        """
        lamb_li = []  # 每种粒子归一化后的λ
        scale_li = []  # 每种粒子的缩放系数scale
        for val in self.m:
            # 当k最大值为100时，概率累加到80时已超过1，因此平均强度归一化到80之内即可
            if val > 0 and val <= 1:
                scale = 80.0
            elif val > 1 and val <= 2:
                scale = 40.0
            elif val > 2 and val <= 3:
                scale = 30.0
            elif val > 3 and val <= 5:
                scale = 16.0
            elif val > 5 and val <= 10:
                scale = 8.0
            elif val > 10 and val <= 20:
                scale = 4.0
            elif val > 20 and val <= 40:
                scale = 2.0
            elif val > 40 and val <= 60:
                scale = 1.5
            elif val > 60 and val <= 80:
                scale = 1.0
            elif val > 80 and val <= 100:
                scale = 0.8
            elif val > 100 and val <= 200:
                scale = 0.4
            elif val > 200 and val <= 300:
                scale = 0.3
            elif val > 300 and val <= 400:
                scale = 0.2
            elif val > 400 and val <= 500:
                scale = 0.16
            elif val > 500 and val <= 800:
                scale = 0.1
            else:
                scale = 0.04

            lamb_li.append(round(val * scale))
            scale_li.append(scale)

        lamb_li = np.array(lamb_li).reshape(1, -1)
        scale_li = np.array(scale_li).reshape(1, -1)
        res_arr = np.concatenate((lamb_li, scale_li), axis=0)
        res_df = pd.DataFrame(res_arr, columns=self.col_name)
        res_df = pd.concat([self.m.to_frame().T, res_df])
        res_df.insert(0, 'metric', value=['avg_ints', 'lambda', 'scale'])
        res_df.set_index(['metric'], inplace=True)  # metric 列作为index
        return res_df

    def poisson(self, k, lamb):
        """
        泊松方程，计算得到单次的概率值。在计算最终阈值时需要将概率累加
        :param k: 泊松方程中的阶乘系数
        :param lamb: 即λ，归一化后的λ,一定是整数
        :return: 泊松方程得到的概率
        """
        kjie = 1  # k!的结果
        for i in range(1, k):
            kjie *= i
        lamb = float(lamb)
        pk = np.power(lamb, k) / kjie * np.exp(-lamb)
        return pk

    def get_ints_thr(self):
        """
        根据泊松方程得到的概率值，计算每种同位素的阈值。。
        :return:每种同位素阈值组成的df
        """
        lamb = self.normal_lambda().iloc[1].values.astype('int')
        scale = self.normal_lambda().iloc[2].values
        ints_val = []
        for i in range(len(self.col_name)):
            thr = 0.0
            prob = 0.0
            for k in range(1, 100):
                prob += self.poisson(k, lamb[i])
                if prob >= self.credible:
                    thr = k / scale[i]
                    break
            ints_val.append(thr)
        ints_val = pd.DataFrame(np.array(ints_val).reshape(1, -1), columns=self.col_name)
        return ints_val

    def classifier(self):
        """
        根据每种元素强度的阈值区分颗粒态和溶解态粒子。
        :return: 粒态和溶解态分类结果的df
        """
        resolve = pd.DataFrame()  # 分类后的溶解态粒子数据
        particle = pd.DataFrame()  # 分类后的颗粒态粒子数据
        ints_thr = self.get_ints_thr()
        ints_thr_li = ints_thr.values[0]

        for idx in range(len(self.col_name)):
            single_ptc_df = self.data_df.iloc[:, idx].to_frame()
            single_ptc_particle = single_ptc_df[single_ptc_df >= ints_thr_li[idx]]
            particle = pd.concat([particle, single_ptc_particle], axis=1)

        resolve = self.data_df[pd.isnull(particle)]
        return particle, resolve


class PostProcess:
    """
    非纯样品之外的样品进行 [减背景，计算颗粒数浓度，计算溶解态浓度，添加embedding，计算质量占比] 处理。
    """

    def __init__(self, ptc_df, res_df, isotopes_info, cali_curve_file, TE, V, T, Vf, m, Df, Vi):
        """
        :param ptc_df: 颗粒态数据df
        :param res_df: 溶解态数据df
        :param isotopes_info: 同位素信息文件名
        :param cali_curve_file: 标准曲线文件名
        :param TE：计算参数，手动输入
        :param V: 流速(ml/min)
        :param T: 测试时间(s)
        :param Vf: 定容体积，默认50
        :param Df: 稀释倍数，默认10
        :param m: 称样质量，默认20
        """
        self.ptc_df = ptc_df
        self.res_df = res_df
        self.df_len = len(self.res_df)
        self.col_name = self.ptc_df.columns
        self.iso_info = read_csv_bigint_embedding(os.path.join("..", isotopes_info), index_col=0)
        # self.iso_info["embedding"] = self.iso_info["embedding"].apply(lambda x: int(x))
        self.cali_data = read_csv_bigint_embedding(os.path.join("..", cali_curve_file))
        self.TE = TE
        self.V = V
        self.T = T
        self.Vf = Vf
        self.m = m
        self.Df = Df
        self.Vi = Vi


    def get_background(self):
        """
        计算每种同位素的背景值并返回对应df。
        :return: 背景值组成的df
        """

        BG = pd.DataFrame([np.nanmean(self.res_df, axis=0)] * self.df_len, columns=self.col_name).fillna(0)
        return BG

    def substract_background(self):
        """
        对颗粒态数据减去背景值，删除全空行并返回减背景后的df
        :return: 减背景后的颗粒态粒子组成的df
        """
        BG = self.get_background()
        substract_bg_particle = self.ptc_df - BG
        substract_bg_particle = substract_bg_particle.dropna(axis=0, how='all')
        return substract_bg_particle

    def get_mass_distribution(self):
        """
        对减去背景值的颗粒态粒子的df计算质量分布，并用质量分布代替强度值。
        :return: 颗粒态粒子质量分布组成的df
        """

        mass_factor = self.iso_info['mass_factor']
        particle_df = self.substract_background()
        mass_df = particle_df * 500 * 0.002 * 0.02 / 60 / 1000 * self.TE / 1000000 / mass_factor

        def sum_mass(row):
            """
            计算每个颗粒的总质量。
            :return: 颗粒的总质量
            """
            return np.nansum(row)

        total_mass = mass_df.apply(lambda x: sum_mass(x), axis=1).values

        def divide(row, total):
            """
            计算每个颗粒的质量分布
            :param row: 行
            :param total: 总数
            :return: 颗粒的质量分布
            """
            return row / total

        mass_percentage_df = mass_df.apply(lambda x: divide(x, total_mass), axis=0)
        mass_df = mass_df[self.col_name]
        return mass_df, mass_percentage_df

    def add_embedding(self):
        """
        对颗粒态粒子质量分布组成的df添加embedding。
        :return: 添加embedding的颗粒态粒子组成的df
        """
        mass_df, particle_df = self.get_mass_distribution()
        embedding = self.iso_info['embedding']
        file_name = 'particle.csv'
        # 占比
        bin_emb_li = list()
        for i in range(particle_df.shape[0]):
            ptc = particle_df.iloc[i]
            tmp = 0
            exist_iso = ptc[ptc.notna()].index
            for iso in exist_iso:
                tmp += embedding[iso]
            bin_emb_li.append(tmp)
        particle_df['embedding'] = bin_emb_li
        particle_df.to_csv(file_name, index=None)
        self.get_particle_percent(particle_df)
        # 质量
        particle_mass_filename = "particle_mass.csv"
        bin_emb_li = list()
        for i in range(mass_df.shape[0]):
            ptc = mass_df.iloc[i]
            tmp = 0
            exist_iso = ptc[ptc.notna()].index
            for iso in exist_iso:
                tmp += embedding[iso]
            bin_emb_li.append(tmp)
        mass_df['embedding'] = bin_emb_li
        mass_df.to_csv(particle_mass_filename, index=None)
        print("Particle file has been savesd.")
        return particle_df

    def get_particle_percent(self, substance_df):
        substance_df = substance_df.drop(['embedding'], axis=1)
        columns = substance_df.columns
        z = substance_df[columns]
        x = z[z.count(axis=1) == 1]

        elemental_df = x.count(axis=0)
        # elemental_df = elemental_df[elemental_df > 0]
        len = elemental_df.index.size

        y = elemental_df.values
        x = pd.DataFrame(y.reshape(1, len), columns=elemental_df.index, index={0})
        x = x * self.Df * 60 * self.Vf / (self.TE * self.V * self.T * self.m)
        # x = x[x > 0]
        sum = x.sum(1)

        data = []
        for i in x.columns:
            data.append(float(x[i] / sum))

        x.loc[1] = data
        x.loc[1] = x.loc[1].apply(lambda i: format(i, '.2%'))
        x["SUM"] = sum
        x.to_csv("count_particle_" + origin_filename[:-4] + ".csv", index=False)

    def get_particle_number(self):
        """
        计算分类后的颗粒态数量。
        :return:
        """
        res = self.add_embedding()['embedding'].to_frame()
        ptc_num = pd.DataFrame(res.count())
        print(type(ptc_num))
        print(ptc_num)
        ptc_num.columns = ['particle count']
        file_name = "single-number.csv"
        ptc_num.to_csv(file_name, index=False)
        print("Nanoparticle's number has been computed.")

    def get_single_element_particle_number(self):
        """
        统计纳米颗粒中的单元素颗粒数量，并保存在single-number.csv中
        :return:
        """
        particle_filename = "particle.csv"
        particle_mass_filename = "particle_mass.csv"
        print(read_csv_bigint_embedding(particle_filename).iloc[:, -1])
        log_emb = read_csv_bigint_embedding(particle_filename).iloc[:, -1].apply(lambda x: math.log2(x)).tolist()
        single_flag = [i.is_integer() for i in log_emb]
        single_number_df = pd.DataFrame({'single_element_particle_count': [single_flag.count(True)]})
        single_number_filename = 'single-number.csv'
        count_df = read_csv_bigint_embedding(single_number_filename)
        count_df = pd.concat([count_df, single_number_df], axis=1)
        count_df.to_csv(single_number_filename, index=False)
        print("Single element particles' number has been computed.")
        return single_number_filename, particle_filename, particle_mass_filename

    def select_columns(self, target_particle):
        """
        在减去背景的颗粒态数据中选择要处理的同位素，组成df并返回
        target_particle：要选择的粒子名列表，如:['27Al','206Pb']。手动输入
        """
        ptc_df = self.substract_background()
        ptc_name_full_li = ptc_df.columns.tolist()  # 表头
        ptc_name_short_li = list(map(lambda x: x[1:-8], ptc_name_full_li))  # 粒子名：原子质量+元素名
        # print(ptc_name_full_li)
        # print(1111111111111111111111111111111111111)
        # print(ptc_name_short_li)
        select_col_li = []  # select_col_li 选中元素所在列的完整列名

        for item in target_particle:
            for i in range(len(ptc_name_full_li)):
                if item == ptc_name_full_li[i]:
                    select_col_li.append(ptc_name_full_li[i])

        selected_ptc_df = ptc_df[select_col_li]
        return selected_ptc_df

    def get_isotopes_number(self, selected_ptc_df):
        """
        计算去除背景后颗粒态的目标同位素的颗粒数。
        :param selected_ptc_df：筛选出的要计算数量的颗粒态粒子d
        """
        number_filename = "number.csv"
        single_particle_filename = "count_particle_" + origin_filename[:-4] + ".csv"
        number_detection_limits_filename = "number_detection_limits.csv"  #数浓度检测限

        ptc_cnt = selected_ptc_df.count()
        res = ptc_cnt * self.Df * 60 * self.Vf / (self.TE * self.V * self.T * self.m)
        ptc_num_con = res.to_frame().T

        ptc_num_con = pd.DataFrame(ptc_num_con)
        ptc_num_con.loc[1] = ptc_num_con.loc[0]
        ptc_num_con.loc[2] = ptc_num_con.loc[0]

        single_df = read_csv_bigint_embedding(single_particle_filename)

        for i in range(len(ptc_num_con.columns)):
            ptc_num_con.loc[1][i] = float(single_df.loc[0][i])
            ptc_num_con.loc[2][i] = ptc_num_con.loc[0][i] - float(single_df.loc[0][i])

        ptc_num_con.index = ["Total", "Single-element", "Multi-elements"]
        ptc_num_con.to_csv(number_filename)
        # ptc_num_con = read_csv_bigint_embedding(number_filename, index_col=0)
        # print(ptc_num_con.index)

        number_detection_limits_con = ptc_num_con.iloc[0].to_frame().T
        number_detection_limits_con.to_csv(number_detection_limits_filename, index=False)

        print("Particle number have been computed.")
        return single_particle_filename, number_filename, number_detection_limits_filename

    def get_mass_detection_limits(self, thr):
        """
        计算质量检测限
        :param thr: iteration算出来的阈值
        """
        mass_detection_limits_filename = "mass_detection_limits.csv"

        slope = self.cali_data['slope (cps/ppb)']
        slope = slope.values

        mass_detection_limits = (500*thr / slope) *0.002 * self.V * self.TE / 60

        print(mass_detection_limits)

        m_d_l = pd.DataFrame([mass_detection_limits], columns=self.col_name)
        m_d_l.to_csv(mass_detection_limits_filename, index = False)
        return mass_detection_limits_filename

    def get_res_concentration(self):
        res_cps = self.res_df.sum(skipna=True) / 75200 / 0.002
        final_res = []
        final_fn = 'Diss. Conc.csv'
        # cali_data = read_csv_bigint_embedding(cali_curves)
        for i in res_cps.index:
            el_name = "[" + i + "]+"
            el_rescps = res_cps[i]
            # print(f'el_name:{el_name};el_rescps:{el_rescps}')
            intercept = 0
            slope = 1
            kb_res = self.cali_data.loc[self.cali_data['analyte'] == el_name]
            # print(kb_res)
            try:
                intercept = kb_res.iat[0, 1]
                slope = kb_res.iat[0, 2]
                intercept = float(intercept)
                slope = float(slope)
                # print(f'intercept:{intercept};slope:{slope}')
            except IndexError:
                print(el_name + " not in calibration_curves.csv")
            res_conc = (el_rescps - intercept) / slope
            final_res.append((el_name, res_conc))
        with open(final_fn, mode='w', newline='') as file:
            writer = csv.writer(file)
            # 写入列名
            writer.writerow(['analyte', 'Diss. Conc. (ppb)'])
            # 写入每一行的数据
            writer.writerows(final_res)
        print("溶解态浓度计算完毕！")
        return final_fn
