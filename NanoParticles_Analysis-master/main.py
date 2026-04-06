import ast
import json
import os
import shutil
from fastapi import FastAPI
import uvicorn

import pandas as pd

from fingerprint_analysis import AprioriProcess, FIAnalysis, FingerprintExtract, FPAnalysis, HeatMapGenerator, has_isotopes
from particle_classify import DataLoader, IterMethod, PoissonMethod, PostProcess, get_isotopes_info, get_TE, \
    get_mass_factor
from similarity_difference_analysis import SimilarityDifferenceAnalysis
from trace_to_source import BaseModel
from const import isotopes_li


path = r'F:\data\\'
# path = r'E:\\'
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)

app = FastAPI()


@app.post("/api/setDirectory")
def set_directory(dir: str):
    """
    定义文件夹路径，之后生成的文件均会存储于该文件夹下
    :param dir: 文件夹路径，例如：/Users/vog/Downloads/test
    :return: 定义的文件夹路径
    """
    os.chdir(dir)
    return dir


@app.post("/api/backRootDirectory")
def back_root_directory():
    """
    进入根目录文件夹
    :return: 根目录文件夹
    """
    os.chdir(path)
    return path


@app.post("/api/enterBatchDirectory")
def enter_Batch_Directory(batch: str):
    """
    进入某一批次的文件夹，若该批次文件夹不存在，则在根目录下新建批次文件夹
    :param batch: 批次号，例如：1
    :return: 当前批次文件夹的路径
    """
    file = path + batch
    file_path = file + '\\'
    os.chdir(path)
    if not os.path.exists(batch):
        os.mkdir(file)
    os.chdir(file_path)
    print("enter************" + str(os.getcwd()))
    return file_path


# stage 1

@app.post("/api/stage1/getIsotopesInfo")
def get_isotopes(batch: str,cali_curve_file: str, mass_factor_file: str = "mass_factor_file.csv"):
    """
    读取标准曲线文件，生成mass_factor
    读取mass_factor，并生成同位素embedding，将同位素的单位强度和embedding存在一个csv文件中。
    注：同位素文件中的同位素按照元素周期表顺序升序排。该文件应为csv，放在当前目录下
    :param batch: 所在批次
    :param cali_curve_file: 标准曲线文件名
    :param mass_factor_file: 同位素文件名
    :return: isotopes_info.csv文件所在的文件夹路径
    """
    #进入目标文件夹
    enter_Batch_Directory(batch)

    print("mass_factor************" + str(os.getcwd()))
    try:
        get_mass_factor(cali_curve_file, mass_factor_file)
    except (TypeError, FileNotFoundError):
        return {"code": 1, "result": cali_curve_file + " not exist!"}
    print("iso************" + str(os.getcwd()))
    try:
        isotopes_info = get_isotopes_info(mass_factor_file)
    except (TypeError, FileNotFoundError):
        return {"code": 1, "result": mass_factor_file + " not exist!"}
    return {"code": 0, "result": str(os.path.dirname(os.path.abspath(isotopes_info)))}


@app.post("/api/stage1/iterationClassify")
def iteration_method(batch: str, origin_csv: str, isotopes_info: str, cali_curves: str, TE: float = None, C: float = 1e9,
                     V: float = 0.02, T: float = 150, Vf: float = 50, Df: float = 50, m: float = 20, Vi: float = 0.05):
    """
    使用迭代法对颗粒态粒子进行筛选，并计算TE（对于标准样品）或计算颗粒物浓度（对于真实样品、纯样品、配置样品）
    注：该方法会计算TE值（对于标准样品）/生成number.csv和particle.csv（对于真实样品、纯样品、配置样品）
    :param batch: 所在批次
    :param origin_csv: 需要处理的颗粒物文件名
    :param isotopes_info: 同位素信息文件名
    :param cali_curves: 标准曲线文件名 (calibration_curves.csv)
    :param TE: 标准样品计算出的TE值
    :param C: 数浓度(个/ml)，默认值为1000000000
    :param V: 流速(ml/min)，默认值为0.02
    :param T: 测试时间(s)，默认值为150
    :param Vf: 定容体积，默认50
    :param Df: 稀释倍数，默认10
    :param m: 称样质量，默认20
    :param Vi: 进样体积，默认0.05
    :return:
    格式： ["code":XX,"result":XXX]
    code: 0 (正常情况)，result : TE/生成文件 single-number.csv; number.csv; Diss. Conc.csv; particle.csv; particle_mass.csv）的路径（对于真实样品、纯样品、配置样品）
    code : 1 (缺少xxx_iteration), result : xxx_iteration not exist!
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)
    print("iteration************" + str(os.getcwd()))

    # Step1：为当前文件创建保存生成文件的文件夹，并切换到对应文件夹路径下。
    cls_method = '_iteration'  # 文件夹后缀

    dir_name = origin_csv[:-4] + cls_method

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    print('Directory of %s have been created!' % dir_name)
    try:
        shutil.copyfile(origin_csv, dir_name + '/' + origin_csv)  # 复制原文件到目标文件夹
    except (TypeError, FileNotFoundError):
        res = {"code": 1, "result": str(origin_csv + " not exist!")}
        return res
    os.chdir(dir_name)  # 切换到保存生成文件的目录

    # Step2：执行分类、减背景、(计算TE)和颗粒数浓度
    #  一：预处理
    data_loader = DataLoader(origin_csv, isotopes_info)  # 实例化
    cleaned_data = data_loader.get_cleaned_data()  # 得到清洗后的数据
    metric_data = data_loader.get_basic_metirc(cleaned_data)  # 得到相关指标统计结果
    # 二：Iteration执行
    itermethod = IterMethod(cleaned_data, metric_data)  # 实例化
    itermethod.iterator()  # 迭代过程
    ptc_df, res_df, thr = itermethod.get_final_result()  # 得到最终的颗粒态数据，将最终的文件复制并返回文件名

    # Step3：减背景、颗粒数浓度、溶解态浓度
    if ptc_df.shape[1] == 1 and TE is None:  # 标准样品， 且没有TE值的时候,计算TE
        ori_TE = get_TE(ptc_df, C, V, T)
        for key, val in ori_TE.items():
            for key2, val2 in val.items():
                TE = val2
        res = TE
    else:  # 非标准样品
        postpro = PostProcess(ptc_df, res_df, isotopes_info, cali_curves, TE=TE, V=V, T=T, Vf=Vf, m=m, Df=Df, Vi=Vi)
        postpro.get_particle_number()
        single_number_filename, particle_filename, particle_mass_filename = postpro.get_single_element_particle_number()
        selected_ptc_df = postpro.select_columns(isotopes_li)
        count_particle_filename, number_filename, number_detection_limits_file = postpro.get_isotopes_number(selected_ptc_df)
        mass_detection_limits_filename = postpro.get_mass_detection_limits(thr)
        res_concentration = postpro.get_res_concentration()  # 溶解态浓度
        res = (
            # os.path.abspath(count_particle_filename),
            os.path.abspath(single_number_filename),
            os.path.abspath(number_filename),
            os.path.abspath(res_concentration),
            os.path.abspath(particle_filename),
            os.path.abspath(particle_mass_filename),
            os.path.abspath(number_detection_limits_file)
        )
    res = {"code": 0, "result": res}
    # Step4：返回上级目录
    print('-' * 50)
    os.chdir('../')
    # return json.loads(res)
    return res


@app.post("/api/stage1/poissonClassify")
def poisson_method(batch: str, origin_csv: str, isotopes_info: str, cali_curves: str, credible: float = 0.997, TE: float = None,
                   C: float = 1e9, V: float = 0.02, T: float = 150, Vf: float = 50, Df: float = 50, m: float = 20, Vi: float = 0.05):
    """
    TODO: 输出变化，加入溶解态计算
    使用泊松法对颗粒态粒子进行筛选，并计算TE（对于标准样品）或计算颗粒物浓度（对于真实样品、纯样品、配置样品）
    注：该方法会计算TE值（对于标准样品）/生成number.csv和particle.csv（对于真实样品、纯样品、配置样品）
    :param batch: 所在批次
    :param origin_csv: 需要处理的颗粒物文件名
    :param isotopes_info: 同位素信息文件名
    :param cali_curves: 标准曲线文件名 (calibration_curves.csv)
    :param credible: 泊松分布的置信度，默认值为0.997
    :param TE: 标准样品计算出的TE值
    :param C: 数浓度(个/ml)，默认值为1000000000
    :param V: 流速(ml/min)，默认值为0.02
    :param T: 测试时间(s)，默认值为150
    :param Vf: 定容体积，默认50
    :param Df: 稀释倍数，默认10
    :param m: 称样质量，默认20
    :param Vi: 称样质量，默认0.05
    :return:
    格式： ["code":XX,"result":XXX]
    code: 0 (正常情况)，result : TE（对于标准样品）/生成文件（single-number.csv & number.csv & Diss. Conc.csv & particle.csv）的路径（对于真实样品、纯样品、配置样品）
    code : 1 (缺少xxx_poisson), result : xxx_poisson not exist!
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("poisson************" + str(os.getcwd()))
    # Step1：为当前文件创建保存生成文件的文件夹，并切换到对应文件夹路径下
    cls_method = '_poisson'  # 文件夹后缀。分类方法不同导致创建的文件夹后缀不同

    dir_name = origin_csv[:-4] + cls_method

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    print('Directory of %s have been created!' % dir_name)
    try:
        shutil.copyfile(origin_csv, dir_name + '/' + origin_csv)  # 复制原文件到目标文件夹
    except (TypeError, FileNotFoundError):
        res = {"code": 1, "result": str(origin_csv + " not exist!")}
        return res
    os.chdir(dir_name)  # 切换到保存生成文件的目录

    # Step2：执行分类、减背景、(计算TE)和颗粒数浓度
    #  一：预处理
    data_loader = DataLoader(origin_csv, isotopes_info)  # 实例化
    cleaned_data = data_loader.get_cleaned_data()  # 得到清洗后的数据
    metric_data = data_loader.get_basic_metirc(cleaned_data)  # 得到相关指标统计结果
    # 二：Poisson执行
    poissonmethod = PoissonMethod(cleaned_data, metric_data, credible)  # 实例化
    ptc_df, res_df = poissonmethod.classifier()  # 分类得到颗粒态和溶解态数据csv

    # Step3：减背景、颗粒数浓度、溶解态浓度
    if ptc_df.shape[1] == 1 and TE is None:  # 标准样品，且 TE 是 None 的时候， 计算TE
        ori_TE = get_TE(ptc_df, C, V, T)
        for key, val in ori_TE.items():
            for key2, val2 in val.items():
                TE = val2
        res = TE
    else:  # 非标准样品
        postpro = PostProcess(ptc_df, res_df, isotopes_info, cali_curves, TE=TE, V=V, T=T, Vf=Vf, m=m, Df=Df, Vi=Vi)
        postpro.get_particle_number()
        single_number_filename, particle_filename, particle_mass_filename = postpro.get_single_element_particle_number()
        selected_ptc_df = postpro.select_columns(isotopes_li)
        count_particle_filename, number_filename = postpro.get_isotopes_number(selected_ptc_df)
        res_concentration = postpro.get_res_concentration()  # 溶解态浓度
        res = (
            # os.path.abspath(count_particle_filename),
            os.path.abspath(single_number_filename),
            os.path.abspath(number_filename),
            os.path.abspath(res_concentration),
            os.path.abspath(particle_filename),
            os.path.abspath(particle_mass_filename)
        )
    res = {"code": 0, "result": res}
    # Step4：返回上级目录
    print('-' * 50)
    os.chdir('../')
    # return json.loads(res)
    return res


# stage 2
@app.post("/api/stage2/getSupportFile")
def get_support_file(batch: str, substance_name: str, support: float = None, pure_flag: bool = False, iter_flag: bool = True):
    """
    根据物质名称、support值（x）以及物质类别（是否为纯物质）生成support_x.csv文件
    :param batch: 所在批次
    :param substance_name: 物质名
    :param support: 支持度
    :param pure_flag: 是否为纯物质，纯物质为true，非纯物质则false，默认为false
    :param iter_flag: 是否采用迭代法
    :return:  格式： ["code":XX,"result":XXX]
              code : 0 (正常结果)， result ： support_x.csv文件所在的文件夹路径
              code : 1 (缺少必要文件) , result:"xxx(文件名) not exist!"
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("support************" + str(os.getcwd()))
    ap = AprioriProcess(substance_name, support, pure_flag=pure_flag, iter_flag=iter_flag)
    step1 = ap.apriori_final()
    # if isinstance(step1, str):
    #     return step1
    # return os.path.abspath(ap.dir_name)
    if isinstance(step1, str):
        res = {"code": 1, "result": str(step1)}
    else:
        res = {"code": 0, "result": os.path.abspath(ap.dir_name)}
    return res


@app.post("/api/stage2/getTestFile")
def get_test_file(batch: str, cali_curves: str, substance_name: str, support: float, TE: float, Vf: float = 50, Df: float = 10, m: float = 20,
                  V: float = 0.02, T: float = 150, iter_flag: bool = True):
    """
    对于真实样品和配置样品，对频繁项进行统计，并生成测试集（test.csv）
    :param batch: 所在批次
    :param cali_curves: 标准曲线文件名 (calibration_curves.csv)
    :param substance_name: 物质名
    :param support: 支持度，建议 [0.003,0.009]
    :param TE: 传输效率
    :param Vf: 定容体积，默认50
    :param Df: 稀释倍数，默认10
    :param m: 称样质量，默认20
    :param V: 流速(ml/min)，默认值为0.02
    :param T: 测试时间(s)，默认值为150
    :param iter_flag: 是否采用迭代法
    :return:  格式： ["code":XX,"result":XXX]
              code : 0 (正常结果)， result ： test_x.csv所在的文件夹路径（x为支持度）
              code : 1 (缺少必要文件) , result:"xxx(文件名) not exist!"
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("test************" + str(os.getcwd()))
    fia = FIAnalysis(substance_name, support, iter_flag)
    # 判断是否有同位素
    ud = not has_isotopes(cali_curves)
    step2 = fia.fi_analysis(ud=ud, TE=TE, V=V, T=T, Vf=Vf, m=m, Df=Df)
    # if isinstance(step2, str):
    #     return step2
    # return os.path.abspath(fia.dir_name)
    if isinstance(step2, str):
        res = {"code": 1, "result": str(step2)}
    else:
        res = {"code": 0, "result": os.path.abspath(fia.dir_name)}
    return res


@app.post("/api/stage2/getHeatmapFile")
def get_heatmap_file(batch: str, substance_name: str, support: float, base: float, Vi: float = 0.05, V: float = 0.02,
                     T: float = 150, iter_flag: bool = True):
    """
    对于真实样品和配置样品，对频繁项进行统计，并生成测试集（test.csv）和热力图文件（HeatMap.csv）
    :param batch: 所在批次
    :param substance_name: 物质名
    :param support: 支持度，建议 [0.003,0.009]
    :param base: log的底数
    :param Vi: 进样体积，默认0.05
    :param V: 流速(ml/min)，默认值为0.02
    :param T: 测试时间(s)，默认值为150
    :param iter_flag: 是否采用迭代法
    :return: HeatMap_base=x_support=x.csv文件所在的文件夹路径，如果缺少必要文件，返回"xxx(文件名) not exist!"
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("heatmap************" + str(os.getcwd()))
    hpg = HeatMapGenerator(substance_name, support, iter_flag)
    state = hpg.heat_map_file(base=base, Vi=Vi, V=V, T=T)
    if isinstance(state, str):
        res = {"code": 1, "result": str(state)}
    else:
        heatmap_file = ''.join([hpg.dir_name, '/HeatMap_', 'base=', str(base), '_support=', str(hpg.support)[:5], '.csv'])
        # print(heatmap_file)
        res = {"code": 0, "result": os.path.abspath(heatmap_file)}
    return res
    # return os.path.abspath(hpg.dir_name)


@app.post("/api/stage2/setNewGroup")
def set_new_group(batch: str, substance_support_str: str, base: float, TE: float, Vi: float = 0.05, V: float = 0.02, T: float = 150,
                  Vf_list_str: str = '', Df_list_str: str = '', m_list_str: str = ''):
    """
    对于纯样品，建立新的分组，并在分组文件夹内生成fp_x.csv(3), HeatMap_x.csv(3), train.csv & configuration_samples_label.csv
    :param batch: 所在批次
    :param substance_support_str: 所有纯样品文件夹名称和该种纯样品支持度的字典字符串（字典按照纯样品入库时顺序），例如：{"meihui_iteration": 0.006, "turang_iteration": 0.005, "weiqi_iteration": 0.008}
    :param base: log的底数
    :param TE: 传输效率
    :param Vi: 进样体积，默认0.05
    :param V: 流速(ml/min)，默认值为0.02
    :param T: 测试时间(s)，默认值为150
    :param Vf_list_str: 定容体积列表，[50, 50, 50]
    :param Df_list_str: 稀释倍数列表，[10, 10, 10]
    :param m_list_str: 称样质量列表，[20, 20, 20]
    :return: 格式： ["code":XX,"result":XXX]
              code : 0 (正常结果)， result ： 生成的density数据以及文件的路径（即分组目录）（二者使用*隔开）
              code : 不是0时 (缺少必要文件) , result:"xxx(文件名) not exist!"
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("group************" + str(os.getcwd()))
    substance_support_dic = ast.literal_eval(substance_support_str)
    group = ""
    for val in substance_support_dic.values():
        param = str(val)[-3:]
        group = ''.join([group, param])

    # 1.对纯样品的频繁项作TFIDF，此时由support参数组合形成对应的分组，并生成指纹
    fe = FingerprintExtract(substance_support_dic, number=3)
    step1 = fe.get_fingerprints()
    if isinstance(step1, str):
        res = {"code": 1, "result": step1}
        return res
    # 2.对指纹进行分析，并生成该support组合对应的训练集，每种纯样品的热力图文件，以及单位质量的颗粒数
    Vf_list = ast.literal_eval(Vf_list_str)
    Df_list = ast.literal_eval(Df_list_str)
    m_list = ast.literal_eval(m_list_str)

    sub_li = [sub.split('_')[0] for sub in substance_support_dic.keys()]
    fpa = FPAnalysis(group, sub_li)
    step2 = fpa.fp_analysis(TE=TE, V=V, T=T, Vf_list=Vf_list, Df_list=Df_list, m_list=m_list)

    if isinstance(step2, str):
        res = {"code": 2, "result": step2}
        return res
        # return step2
    fpa.heat_map_file(base=base, Vi=Vi, V=V, T=T)
    ori_mass_density = fpa.get_mass_density(mass_list=m_list)

    temp_dict = dict()
    for key, val in ori_mass_density.items():
        for key2, val2 in val.items():
            temp_dict.update({key: val2})
    sub_res1 = str(temp_dict)
    sub_res2 = os.path.abspath(fe.group_dir)

    step3 = fpa.configuration_samples_label()
    if isinstance(step3, str):
        res = {"code": 2, "result": step3}
        return res

    # res = {"code": 0, "result": sub_res1 + "*" + sub_res2}
    res = {"code": 0, "result": [sub_res1, sub_res2]}
    return res


# stage 3
@app.post("/api/stage3/updateModel")
def update_model(batch: str, pure_sample_li_str: str, group: str, clf_model: str):
    """
    根据纯物质组的三种物质、这三种物质所在的目录以及params生成模型文件model.m和标准化参数文件sc.bin
    :param batch: 所在批次
    :param pure_sample_li_str: 纯物质列表字符串，例如：["meihui", "turang", "weiqi"]
    :param group: 分组目录名(训练集在该目录下)
    :param clf_model: 选择训练的模型名称，例如：RFModel, SVMModel, GaussianNBModel, XGBoostModel
    :return: model.m&sc.bin文件所在的文件夹路径（即分组目录）
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("model************" + str(os.getcwd()))
    pure_sample_li = ast.literal_eval(pure_sample_li_str)
    if clf_model == 'RFModel':
        params = {'n_estimators': 10, 'random_state': 1024}
    elif clf_model == 'SVMModel':
        params = {'C': 0.8, 'kernel': 'linear', 'decision_function_shape': 'ovr'}
    elif clf_model == 'GaussianNBModel':
        params = {}
    elif clf_model == 'XGBoostModel':
        params = {}
    clf = BaseModel(pure_sample_li, clf_model, sample_support=None)
    train_state = clf.train_model(group, **params)
    # if isinstance(train_state, str):
    #     return train_state
    # return os.path.abspath(clf_model)
    if isinstance(train_state, str):
        return {"code": 1, "result": train_state}
    model_path = os.path.abspath(os.path.join(group, clf_model))
    res = {"code": 0, "result": model_path}
    return res


@app.post("/api/stage3/traceToSource")
def trace_to_source(batch: str, pure_sample_li_str: str, model: str, test_sample_str: str, clf_model: str, support_li_str: str,
                    test_sample_id_li_str: str, iter_flag: bool = True):
    """
    根据纯物质组的三种物质、模型名称（使用这三种物质所在的目录名）以及需要溯源的文件名生成溯源文件trace_result.csv
    :param batch: 所在批次
    :param pure_sample_li_str: 纯物质列表字符串，例如：["meihui", "turang", "weiqi", "unknown"]
    :param model: 分组目录名（模型在该目录下）
    :param test_sample_str: 要溯源的样品名列表字符串，例如：["A1", "A3", "A5"]
    :param clf_model: 选择训练的模型名称，例如：RFModel, SVMModel, GaussianNBModel, XGBoostModel
    :param support_li_str: 非纯样品的支持度列表字符串，例如：[0.001, 0.02, 0.003]
    :param test_sample_id_li_str: 要溯源的样品id列表字符串
    :param iter_flag: 是否采用迭代法
    :return: trace_result.csv文件所在的文件夹路径（即分组目录）
    """
    # 进入目标文件夹
    enter_Batch_Directory(batch)

    print("trace************" + str(os.getcwd()))
    pure_sample_li = ast.literal_eval(pure_sample_li_str)
    test_sample_li = ast.literal_eval(test_sample_str)
    support_li = ast.literal_eval(support_li_str)
    test_sample_id_li = ast.literal_eval(test_sample_id_li_str)
    for i, (sample, support, sample_id) in enumerate(zip(test_sample_li, support_li, test_sample_id_li)):
        clf = BaseModel(pure_sample_li, clf_model, sample_support=float(support), iter_flag=iter_flag)
        test_state = clf.run(model, sample, sample_id, first=(i == 0))
        if isinstance(test_state, str):
            return {"code": 1, "result": test_state}
    model_path = os.path.abspath(os.path.join(model, clf_model))
    return {"code": 0, "result": model_path}
    #     if isinstance(test_state, str):
    #         return test_state
    # return os.path.abspath(clf_model)


@app.post("/api/stage3/similarityDifferenceAnalysis")
def similarity_difference_analysis(element_for_filter_str: str, dir_path: str):
    """
    指纹异同分析，用户上传一系列csv文件，存在dir_path文件夹下，输入需要筛选的元素列表，输出三个结果文件路径，不需要存储历史记录
    :param element_for_filter_str: 需要筛选的元素列表字符串如["Na","Mg","Al"]，可以为空数组
    :param dir_path: 用户上传文件所存的文件夹
    :return: ["code":XX,"result":XXX]
              code : 0 (正常结果)， result ：返回值为csv文件路径构成的list，依次为all.csv, selected-dominated.csv, selected-non-dominated.csv，如果element_for_filter_str为空，则只有第一个
              code : 1 (筛选元素不在上传的csv文件中) , result:"['xxx', 'xxx'](元素名) not in index"
    """
    element_for_filter = ast.literal_eval(element_for_filter_str)
    if len(element_for_filter) == 0:
        element_for_filter = None
    sda = SimilarityDifferenceAnalysis()
    try:
        output_filenames = sda.sd_analysis(dir_path, element_for_filter)
    except KeyError as err:
        return {"code": 1, "result": str(err)}
    # return [os.path.abspath(filename) for filename in output_filenames]
    res = [os.path.abspath(filename) for filename in output_filenames]
    # return json.dumps(res)
    return {"code": 0, "result": res}
