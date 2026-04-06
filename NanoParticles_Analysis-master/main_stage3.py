#!/usr/bin/python3
# author Yates

"""
该脚本测试第三阶段功能，对对应代码在’trace_to_source.py‘
"""

import os

os.chdir('/Users/zhangyunqi/PycharmProjects/0_Nano/dataset/原始数据')

from trace_to_source import BaseModel


def main():
    # for clf_model in clf_models:
    if clf_model == 'RFModel':
        params = {'n_estimators': 10, 'random_state': 1024}
    elif clf_model == 'SVMModel':
        params = {'C': 0.8, 'kernel': 'linear', 'decision_function_shape': 'ovr'}
    elif clf_model == 'GaussianNBModel':
        params = {}
    elif clf_model == 'XGBoostModel':
        params = {}
    # for train_group in group:
    if update:  # 更新模型
        pure_sample_li = ['meihui', 'turang', 'weiqi']
        clf = BaseModel(pure_sample_li, clf_model, sample_support=sample_support)
        train_state = clf.train_model(train_group, **params)
        if isinstance(train_state, str):
            return train_state
    else:  # 溯源样品
        pure_sample_li = ['meihui', 'turang', 'weiqi', 'unknown']
        clf = BaseModel(pure_sample_li, clf_model, sample_support=sample_support)
        # for sample in test_sample:
        test_state = clf.run(train_group, test_sample)
        if isinstance(test_state, str):
            return test_state


# 控制机器学习模型阶段：True-->训练; False-->测试
update = True
# clf_models = ['RFModel', 'SVMModel', 'GaussianNBModel', 'XGBoostModel']
clf_model = 'RFModel'
# group = ['005004007']
train_group = '005004007'

sample_support = 0.01  # 非纯样品的support，测试输入support值下的非纯样品，用于定位测试集文件

# 从文件夹中得到测试集
# 测试文件都放在test_sample文件夹下
test_sample = 's1'
# test_dir = 'test_sample/'
# test_files = os.listdir(test_dir)
# for test_f in test_files:
#     test_sample.append(test_f.split('_')[0])

if __name__ == '__main__':
    main()
