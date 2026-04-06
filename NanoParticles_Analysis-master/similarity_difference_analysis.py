import os
import re

import pandas as pd
from const import isotopes_li


# ISOTOPES = ['24Mg', '27Al', '42Ca', '44Ca', '46Ti', '47Ti', '48Ti', '49Ti', '50Ti', '51V', '52Cr', '54Fe', '55Mn',
#             '57Fe', '58Fe', '59Co', '60Ni', '63Cu', '66Zn', '75As', '82Se', '86Sr', '87Sr', '88Sr', '89Y', '95Mo',
#             '98Mo', '104Pd', '105Pd', '107Ag', '111Cd', '112Sn', '121Sb', '138Ba', '139La', '140Ce', '141Pr',
#             '146Nd', '147Sm', '153Eu', '157Gd', '159Tb', '163Dy', '165Ho', '166Er', '169Tm', '172Yb', '175Lu',
#             '182W', '195Pt', '197Au', '205Tl', '206Pb', '207Pb', '208Pb']


def read_csv_bigint_embedding(file, index_col=None):
    df = pd.read_csv(file, index_col=index_col)
    if "embedding" in df:
        df["embedding"] = df["embedding"].apply(lambda x: int(x))
    return df


class SimilarityDifferenceAnalysis:
    def __init__(self):
        self.iso_emb = None
        self.samples_info = None
        self.samples_name = None
        self.dir_path = None
        self.get_isotopes_embedding()
        self.res_dir = "sd_analysis"
        if not os.path.exists(self.res_dir):
            os.mkdir(self.res_dir)

    def get_isotopes_embedding(self):
        """
        读取同位素单位强度文件，并生成同位素embedding
        注：同位素文件中的同位素按照元素周期表顺序升序排。
        :return:
        """
        embedding = {}
        for i, iso in enumerate(isotopes_li):
            embedding[iso] = 1 << i
        # print(emb)
        self.iso_emb = pd.DataFrame(embedding, columns=isotopes_li, index=[0])
        # print(self.iso_emb)

    # def calculate_new_embedding(self):
    #     embedding = []
    #     for idx in self.samples_info.index:
    #         # print(idx)
    #         component = self.samples_info.loc[idx, "component"]
    #         emb = self.encode_embedding(component)
    #         embedding.append(emb)
    #         # print(component, emb, self.decode_embedding(emb))
    #     self.samples_info["new_embedding"] = embedding

    def read_samples(self, element_for_filter=None):
        """
        读取所有test文件，处理得到[sample, component, number]
        :return:
        """
        self.samples_info = pd.DataFrame(columns=["sample", "new_embedding", "number"])
        self.samples_name = []
        for file in os.listdir(self.dir_path):
            if file.endswith(".csv"):
                sample_name = file.replace(".csv", "")

                # 获取样品相关信息
                ori_info = read_csv_bigint_embedding(os.path.join(self.dir_path, file))

                if element_for_filter is None:
                    info = ori_info[["component", "number"]].dropna()
                else:
                    # 如果不为空，number为选中的元素浓度最小值
                    info = ori_info[element_for_filter + ["component"]].dropna()
                    info = info[~(ori_info[element_for_filter] == 0).any(axis=1)]  # 删除满足条件的行
                    info["number"] = info[element_for_filter].min(axis=1)
                    info = info.drop(columns=element_for_filter)

                # 如果info中行数==0，则不考虑该元素
                if info.shape[0] == 0:
                    print("样品" + sample_name + "筛选后，行数为0，不进行输出")
                    continue

                self.samples_name.append(sample_name)

                # 处理component为list，并计算新的embedding
                info = info.rename(columns={'component': 'new_embedding'})
                info["new_embedding"] = info["new_embedding"].map(lambda x: int(self.encode_embedding(x.split("-"))))

                # 获取相对于所有元素的embedding，注意这里的embedding和mass_factor的不同
                info["sample"] = sample_name
                self.samples_info = pd.concat([self.samples_info, info], ignore_index=True)

        self.samples_info.to_csv("samples_info.csv")

    def get_columns(self):
        """
        样品名按字典序排序，每个样品名后插入一个number
        :return:
        """

        def get_alpha_str(s):
            result = ''.join(re.split(r'[^A-Za-z]', s))
            return result

        def get_digit_str(s):
            result = ''.join(re.split(r'[^0-9]', s))
            return result

        self.samples_name.sort(key=lambda x: (get_alpha_str(x), int(get_digit_str(x))))
        # print(self.samples_name)
        columns = []
        for item in self.samples_name:
            # if element_for_filter is None:
            columns.extend([item, item + "-number"])
            # else:
            #     columns.extend([item, item + "-number", item + "-" + element_for_filter])
        columns.append("iso_num")
        return columns

    def decode_embedding(self, embedding):
        """
        对embedding解码，得到同位素组合(按原子质量升序排列)。
        :param embedding: 指纹的embedding
        :return: 指纹的同位素组合
        """
        iso_emb = self.iso_emb
        iso_li = list()
        for iso in iso_emb.columns:
            if int(iso_emb[iso][0]) == embedding & int(iso_emb[iso][0]):
                iso_li.append(iso)
        return iso_li

    def encode_embedding(self, iso_set):
        """
        对元素集合进行编码，得到embedding
        :param iso_set:
        :return:
        """
        result = 0
        for iso in iso_set:
            result += self.iso_emb[iso][0]
        # print(iso_set, result)
        return result

    def sd_analysis(self, input_dir, element_for_filter=None):
        """
        :param element_for_filter: 用于筛选row的元素，如果该元素为0，删除其所在行
        :param input_dir: test文件所在目录
        """
        self.dir_path = input_dir
        self.read_samples(element_for_filter)

        # print(len(set(self.samples_info["new_embedding"])))
        # 初始化列名
        columns = self.get_columns()

        # 按频繁项emb进行聚类
        group_by_emb = self.samples_info.groupby(by="new_embedding")
        # for group in group_by_emb:
        #     print(group)
        freq_item_embedding_set = group_by_emb.groups.keys()  # 所有出现过的频繁项embedding

        res_df_all = pd.DataFrame(columns=columns, index=freq_item_embedding_set)
        emb_w_filter_element = []
        emb_wo_filter_element = []

        def has_all_filter_element(freq_item_list):
            for ele in element_for_filter:
                if ele not in freq_item_list:
                    return False
            return True

        for emb in freq_item_embedding_set:
            freq_item = self.decode_embedding(emb)
            # 包含筛选元素的index
            if element_for_filter is not None:
                if has_all_filter_element(freq_item):
                    emb_w_filter_element.append(emb)
                else:
                    emb_wo_filter_element.append(emb)
            samples_with_emb_info = pd.DataFrame(group_by_emb.get_group(emb)).set_index(["sample"], inplace=False)
            sample_with_emb = list(samples_with_emb_info.index)  # 有当前频繁项的样品
            # 将频繁项放进输出
            res_df_all.loc[emb, sample_with_emb] = "-".join(freq_item)
            # 将number放进输出
            for sample in sample_with_emb:
                number_col = sample + "-number"
                res_df_all.loc[emb, number_col] = samples_with_emb_info.loc[sample, "number"]
                # if element_for_filter is not None:
                #     ele_filter_col = sample + "-" + element_for_filter
                #     res_df.loc[emb, ele_filter_col] = samples_with_emb_info.loc[sample, element_for_filter]
            res_df_all.loc[emb, "iso_num"] = len(freq_item)

        # 按频繁项出现次数排序
        res_df_all['sample_number'] = res_df_all.count(axis=1)
        res_df_all_sorted = res_df_all.sort_values('sample_number', ascending=False)
        res_df_all_sorted = res_df_all_sorted.drop(columns=["sample_number"])

        # 重命名列名
        rename_column = []
        for i, c in enumerate(columns):
            if c.endswith("-number"):
                rename_column.append("number")
            # elif element_for_filter is not None and c.endswith("-" + element_for_filter):
            #     rename_column.append(element_for_filter)
            else:
                rename_column.append(c)
        res_df_all_sorted.columns = rename_column

        if element_for_filter is None:
            output_filenames = ["all.csv"]
        else:
            suffix = "-".join(element_for_filter)
            output_filenames = ["all.csv", "selected-dominated-" + suffix + ".csv", "selected-non-dominated-" + suffix + ".csv"]

        output_filenames = [os.path.join(self.res_dir, filename) for filename in output_filenames]

        res_df_all_sorted.to_csv(output_filenames[0], index=False)

        # 包含筛选的元素的指纹 以及 不包含筛选元素的指纹 分别构成的输出
        if element_for_filter is not None:
            res_df_w_filter_element = res_df_all_sorted.loc[res_df_all_sorted.index.isin(emb_w_filter_element)]
            res_df_wo_filter_element = res_df_all_sorted.loc[res_df_all_sorted.index.isin(emb_wo_filter_element)]
            res_df_w_filter_element.to_csv(output_filenames[1], index=False)
            res_df_wo_filter_element.to_csv(output_filenames[2], index=False)
        return output_filenames


if __name__ == '__main__':
    # 修改dir_path为要分析的test文件所在目录，建议test文件名为样品名
    # 如果报路径错误，可以修改为绝对路径
    element_for_filter = ["208Pb"]  # 如果不需要筛选可以修改为：element_for_filter = None
    dir_path = "test_files"
    sda = SimilarityDifferenceAnalysis()
    try:
        output_filenames = sda.sd_analysis(dir_path, element_for_filter)
    except KeyError as err:
        print(err)
