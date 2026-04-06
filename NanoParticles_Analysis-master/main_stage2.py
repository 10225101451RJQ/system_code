#!/usr/bin/python3
# author Yates

"""
该脚本测试第二阶段功能，对对应代码在’fingerprint_analysis.py‘
"""

import os

os.chdir('/Users/zhangyunqi/PycharmProjects/0_Nano/dataset/20230926')

from fingerprint_analysis import has_isotopes, AprioriProcess, FIAnalysis, FingerprintExtract, FPAnalysis, \
    HeatMapGenerator


def main():
    # 配置/真实样品处理流程
    if not pure_flag:
        # 1.先提取频繁项
        ap = AprioriProcess(substance, support)
        step1 = ap.apriori_final()
        if isinstance(step1, str):
            return step1
        # 2.对频繁项进行统计,并生成测试集和热力图文件，fi_analysis的ud参数决定是否对未知源进行检测
        # 判断是否有同位素
        ud = not has_isotopes(cali_curve)
        fia = FIAnalysis(substance, support)
        step2 = fia.fi_analysis(ud=ud, TE=TE, V=V, T=T, Vf=Vf, m=m, Df=Df)
        if isinstance(step2, str):
            return step2
        hpg = HeatMapGenerator(substance, support)
        hpg.heat_map_file(base=base, Vi=Vi, V=V, T=T)

    # 纯样品处理流程
    else:
        if not new_group:  # 不对纯样品建立分组
            # 1.先提取频繁项
            ap = AprioriProcess(substance, support, pure_flag=pure_flag)
            step1 = ap.apriori_final()
            if isinstance(step1, str):
                return step1

        else:  # 建立分组
            # 1.对纯样品的频繁项作TFIDF，此时由support参数组合形成对应的分组，并生成指纹
            fe = FingerprintExtract(substance_support_dic, number=3)
            step1 = fe.get_fingerprints()
            if isinstance(step1, str):
                return step1
            # 2.对指纹进行分析，并生成该support组合对应的训练集，每种纯样品的热力图文件，以及单位质量的颗粒数
            sub_li = [sub.split('_')[0] for sub in substance_support_dic.keys()]
            fpa = FPAnalysis(group, sub_li)
            step2 = fpa.fp_analysis(TE=TE, V=V, T=T, Vf_list=Vf_list, Df_list=Df_list, m_list=m_list)
            if isinstance(step2, str):
                return step2
            fpa.heat_map_file(base=base, Vi=Vi, V=V, T=T)
            fpa.get_mass_density(mass_list=m_list)
            step3 = fpa.configuration_samples_label()
            if isinstance(step3, str):
                return step3


cali_curve = "calibration_curves.csv"

# 是否处理纯样品
pure_flag = False

# 提取频繁项
substance = 'sample'
support = 0.007

# 纯样品是否建立分组（只有纯样品需要）
new_group = True

# 建立分组用到的纯样品文件
substance_support_dic = {'meihui_iteration': 0.004, 'turang_iteration': 0.004, 'weiqi_iteration': 0.007}

# 分组目录名
# group = '005006008'

group = ""
for val in substance_support_dic.values():
    param = str(val)[-3:]
    group = ''.join([group, param])

print(group)

# 生成热力图文件的参数
base = 10  # log的底数，默认是10

Vi = 0.05  # 进样体积
TE = 0.245  # TE要在标准样品计算出结果后再填
C = 1e6  # 数浓度(个/ml)
V = 0.02  # 流速(ml/min)
T = 150  # 测试时间(s)
Vf = 50  # 定容体积
m = 20  # 称样质量
Df = 100  # 稀释倍数

Vf_list = [50, 50, 50]  # 定容体积列表，用于建立分组
Df_list = [100, 100, 100]  # 稀释倍数列表
m_list = [20, 20, 20]  # 称样质量

if __name__ == '__main__':
    print(main())
