#!/usr/bin/python3
# author Yates

"""
该脚本测试第一阶段功能，对对应代码在’particle_classify.py‘
"""

import os
import shutil

import pandas as pd
from const import isotopes_li

os.chdir('/Users/zhangyunqi/PycharmProjects/0_Nano/dataset/原始数据_1')

from particle_classify import (DataLoader, IterMethod, PoissonMethod, PostProcess, get_isotopes_info, get_TE,
                               get_mass_factor)


def main():
    # Step1: 读取同位素单位强度文件，生成包含同位素强度和embedding的csv文件
    try:
        get_mass_factor(cali_curve, mass_factor)
    except (TypeError, FileNotFoundError):
        return cali_curve + " not exist!"
    try:
        isotopes_info = get_isotopes_info(mass_factor)
    except (TypeError, FileNotFoundError):
        return mass_factor + " not exist!"

    # Step1：为当前文件创建保存生成文件的文件夹，并切换到对应文件夹路径下。
    cls_method = '_iteration' if iteration else '_poisson'  # 文件夹后缀。分类方法不同导致创建的文件夹后缀不同

    dir_name = origin_csv[:-4] + cls_method
    print(dir_name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    print('Directory of %s have been created!' % dir_name)
    try:
        shutil.copyfile(origin_csv, dir_name + '/' + origin_csv)  # 复制原文件到目标文件夹
    except (TypeError, FileNotFoundError):
        return origin_csv + " not exist!"
    os.chdir(dir_name)  # 切换到保存生成文件的目录

    # Step2：执行分类、减背景、(计算TE)和颗粒数浓度
    # 迭代法
    if iteration:
        #  一：预处理
        data_loader = DataLoader(origin_csv, isotopes_info)  # 实例化
        cleaned_data = data_loader.get_cleaned_data()  # 得到清洗后的数据
        metric_data = data_loader.get_basic_metirc(cleaned_data)  # 得到相关指标统计结果
        # 二：Iteration执行
        itermethod = IterMethod(cleaned_data, metric_data)  # 实例化
        itermethod.iterator()  # 迭代过程
        ptc_df, res_df, thr = itermethod.get_final_result()  # 得到最终的颗粒态数据，将最终的文件复制并返回文件名
    # 泊松法
    else:
        #  一：预处理
        data_loader = DataLoader(origin_csv, isotopes_info)  # 实例化
        cleaned_data = data_loader.get_cleaned_data()  # 得到清洗后的数据
        metric_data = data_loader.get_basic_metirc(cleaned_data)  # 得到相关指标统计结果
        # 二：Poisson执行
        poissonmethod = PoissonMethod(cleaned_data, metric_data, credible)  # 实例化
        ptc_df, res_df = poissonmethod.classifier()  # 分类得到颗粒态和溶解态数据csv

    # Step3：减背景、颗粒数浓度
    if ptc_df.shape[1] == 1:  # 标准样品，计算TE
        get_TE(ptc_df, C, V, T)
    else:  # 非标准样品
        postpro = PostProcess(ptc_df, res_df, isotopes_info, cali_curve, TE=TE, V=V, T=T, Vf=Vf, m=m, Df=Df, Vi=Vi)
        postpro.get_particle_number()

        single_number_filename, particle_filename, particle_mass_filename = postpro.get_single_element_particle_number()
        # print(os.path.abspath(single_number_filename), os.path.abspath(particle_filename))
        selected_ptc_df = postpro.select_columns(isotopes_li)
        postpro.get_isotopes_number(selected_ptc_df)

        # 计算溶解态浓度
        postpro.get_res_concentration()

    # Step4：返回上级目录
    print('-' * 50)
    os.chdir('../')


# origin_csv = '197Au.csv'  # 标准样品
origin_csv = 's1.csv'  # 非标准样品

mass_factor = 'mass_factor.csv'
cali_curve = "calibration_curves.csv"

Vi = 0.05  # 进样体积
TE = 0.382  # TE要在标准样品计算出结果后再填
C = 1e4  # 数浓度(个/ml)
V = 0.02  # 流速(ml/min)
T = 150  # 测试时间(s)
Vf = 50  # 定容体积
m = 20  # 称样质量
Df = 100  # 稀释倍数

iteration = True
credible = 0.997

# 用于计算溶解态浓度
cali_curves = 'calibration_curves.csv'

if __name__ == '__main__':
    print(main())
