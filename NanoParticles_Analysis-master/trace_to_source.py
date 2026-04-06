#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/17
# @Author  : Li Songda
# @Github  : https://github.com/lisdarr
# @Software: PyCharm
# @File    : trace_to_source.py

import os
import re
import joblib
import pandas as pd
from matminer.featurizers.composition import ElementProperty
from pymatgen.core import Composition
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, naive_bayes
from xgboost.sklearn import XGBClassifier
from const import isotopes_li


def read_csv_bigint_embedding(file, index_col=None):
    df = pd.read_csv(file, index_col=index_col)
    if "embedding" in df:
        df["embedding"] = df["embedding"].apply(lambda x: int(x))
    return df


def isotope_to_element(isotope):
    """
    将同位素转化为元素
    :param isotope: 同位素名，如'27Al'
    :return: 元素名，如'Al'
    """
    return re.search('[A-Za-z]+', isotope).group()


class BaseModel:
    def __init__(self, pure_sample_li, clf_model, sample_support, iter_flag=True):
        """
        :param pure_sample_li: 纯物质列表
        :param iter_flag: 是否是迭代法得到的结果，默认为True。若是泊松法，改为False
        """
        self.pure_sample_li = pure_sample_li
        self.suffix = 'iteration' if iter_flag else 'poisson'  # 要溯源样品所在目录的后缀
        self.mapping = dict()
        self.clf_model = clf_model
        self.support = sample_support

    def build_mapping(self):
        """
        建立纯物质的id映射表
        :return:
        """
        for i, sap in enumerate(self.pure_sample_li):
            self.mapping[sap] = i

    def get_comps(self, row):
        """
        根据频繁项(指纹)的元素分布，得到频繁项(指纹)的化学式
        :param row: 频繁项(指纹)的元素分布
        :return: 该频繁项(指纹)的化学式
        """
        return Composition(''.join([isotope_to_element(i[0]) + str(i[1]) for i in list(row.to_dict().items())]))

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

    def get_train_set(self, group):
        """
        从分组目录中读取train.csv并处理得到训练集和StandardScaler
        :param group: 分组目录名(训练集在该目录下)
        :return: X_train, y_train, std_x
        """
        self.build_mapping()
        path = '/'.join([group, 'train.csv'])
        try:
            train = read_csv_bigint_embedding(path)
        except (TypeError, FileNotFoundError):
            return path + " not exist!"
        # elms_li = train.columns[0:-5]

        elms_li = [col for col in train.columns if col in isotopes_li]
        train[elms_li] = train[elms_li].apply(lambda x: self.get_percentage(x), axis=1)
        train['substance'] = train['substance'].map(self.mapping)
        train = train.sample(frac=1)
        train['formula'] = train[elms_li].apply(self.get_comps, axis=1)
        ep = ElementProperty.from_preset(preset_name='magpie')
        # ep.features = ['Number', '', '', '']
        y_train = train['substance'].values
        X_train = ep.featurize_dataframe(train[['formula']], 'formula').drop('formula', axis=1).values
        std_x = StandardScaler()
        X_train = std_x.fit_transform(X_train)
        return X_train, y_train, std_x

    def get_train_set_resnet(self, group):
        """
        从分组目录中读取train.csv并处理得到训练集
        :param group: 分组目录名(训练集在该目录下)
        :return: X_train, y_train
        """
        self.build_mapping()
        path = '/'.join([group, 'train.csv'])
        train = read_csv_bigint_embedding(path)
        # elms_li = train.columns[0:-5]
        elms_li = [col for col in train.columns if col in isotopes_li]
        train[elms_li] = train[elms_li].apply(lambda x: self.get_percentage(x), axis=1)
        train['substance'] = train['substance'].map(self.mapping)
        # 对数据进行shuffle
        train = train.sample(frac=1)
        train['formula'] = train[elms_li].apply(self.get_comps, axis=1)
        ep = ElementProperty.from_preset(preset_name='magpie')
        # ep.features = ['Number', '', '', '']
        y_train = train['substance'].values
        X_train = ep.featurize_dataframe(train[['formula']], 'formula').drop('formula', axis=1).values
        # StandardScaler: 对训练集进行归一化，测试集同理
        return X_train, y_train

    def get_test_set(self, test_sample):
        """
        从样品目录中读取test.csv并处理得到测试集
        :param test_sample: 要溯源的样品名
        :return: X_test
        """
        self.build_mapping()
        dir_name = '_'.join([test_sample, self.suffix])
        path = '/'.join([dir_name, 'test_' + str(self.support)[:5] + '.csv'])
        try:
            test = read_csv_bigint_embedding(path)
        except (TypeError, FileNotFoundError):
            return path + " not exist!"
        # elms_li = test.columns[0:-5]
        elms_li = [col for col in test.columns if col in isotopes_li]
        test[elms_li] = test[elms_li].apply(lambda x: self.get_percentage(x), axis=1)
        test['formula'] = test[elms_li].apply(self.get_comps, axis=1)
        ep = ElementProperty.from_preset(preset_name='magpie')
        # ep.features = ['Number']
        X_test = ep.featurize_dataframe(test[['formula']], 'formula').drop('formula', axis=1).values
        return X_test

    def get_test_set_resnet(self, test_sample):
        """
        从样品目录中读取test.csv
        :param test_sample: 要溯源的样品名
        :return: X_test
        """
        self.build_mapping()
        dir_name = '_'.join([test_sample, self.suffix])
        path = '/'.join([dir_name, 'test_' + str(self.support)[:5] + '.csv'])
        return path

    def train_model(self, group, **kwargs):
        """
        根据选择的训练集，建立分类器并保存新模型。
        :param group: 分组目录名(训练集在该目录下)
        :param kwargs: 要设置的超参数组成的字典
        :return:
        """
        train_state = self.get_train_set(group)
        if isinstance(train_state, str):
            return train_state
        X_train, y_train, std_x = train_state
        model_dir = ''.join([group, '/', self.clf_model])
        model_file = ''.join([model_dir, '/model', '.m'])  # 模型文件
        std_file = ''.join([model_dir, '/sc.bin'])  # StandardScaler文件

        # 随机森林分类器进行溯源
        if self.clf_model == 'RFModel':
            clf = RandomForestClassifier(**kwargs)
        elif self.clf_model == 'SVMModel':
            clf = svm.SVC(**kwargs)
        elif self.clf_model == 'GaussianNBModel':
            clf = naive_bayes.GaussianNB(**kwargs)
        elif self.clf_model == 'XGBoostModel':
            clf = XGBClassifier(**kwargs)

        # 模型训练
        clf.fit(X_train, y_train)

        # 保存模型
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        joblib.dump(clf, model_file)
        joblib.dump(std_x, std_file)

        print(f'{self.clf_model} {group} and it\'s StancardScaler has been saved')

    def run(self, group, test_sample, test_sample_id="sample_id", first=False):
        """
        运行模型，得到测试样品中频繁项分类结果，并处理为溯源结果并保存
        :param group: 要使用的模型对应的group
        :param test_sample: 要溯源的样品名
        :param test_sample_id: 要溯源的样品id
        :param first: 是否是第一个样品，如果是第一个样品，清空trace_result.csv文件
        :return:
        """
        test_sample_path = test_sample
        X_test = self.get_test_set(test_sample_path)
        if isinstance(X_test, str):
            return X_test
        model_dir = ''.join([group, '/', self.clf_model])
        model_file = ''.join([model_dir, '/model', '.m'])  # 模型文件
        std_file = ''.join([model_dir, '/sc.bin'])  # StandardScaler文件
        clf = joblib.load(model_file)
        std_x = joblib.load(std_file)
        X_test = std_x.transform(X_test)
        res = clf.predict(X_test)
        res_list = res.tolist()
        dir_name = '_'.join([test_sample_path, self.suffix])
        test_path = '/'.join([dir_name, 'test_' + str(self.support)[:5] + '.csv'])
        test = read_csv_bigint_embedding(test_path)
        # diff unknown
        len_res = len(res_list)
        for i in range(len_res):
            if pd.isna(test['substance'][i]):
                test.loc[i, 'substance'] = res[i]
            else:
                test.loc[i, 'substance'] = 3

        inverse_mapping = dict()
        for k, v in self.mapping.items():
            inverse_mapping[v] = k
        test['substance'] = test['substance'].map(inverse_mapping)
        res_df = test[['substance', 'number']].groupby('substance').sum().T
        total = sum(res_df.values[0])
        res_df /= total
        res_dict = res_df.to_dict('records')
        res_dict[0]["id"] = test_sample_id
        final_res = pd.DataFrame(data=res_dict, columns=["id"] + self.pure_sample_li)
        final_res.index = [test_sample + "_support=" + str(self.support)]
        trace_res_file = ''.join([group, '/', self.clf_model, '/trace_results.csv'])  # 记录该分组模型测试结果
        if first or not os.path.exists(trace_res_file):
            final_res.to_csv(trace_res_file)
        else:  # trace_results.csv存在则追加写入结果
            all_res_df = read_csv_bigint_embedding(trace_res_file, index_col=0)
            all_res_df = pd.concat([all_res_df, final_res])
            all_res_df = all_res_df.sort_index()
            all_res_df.to_csv(trace_res_file)
        print(f'Traceability of {test_sample} in {self.clf_model} has been finished.')
