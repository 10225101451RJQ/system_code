## 机器&实验参数
* *C<sub>p</sub>*: 数浓度(个/L)
* *V*: 流速(ml/min)
* *T*: 测试时间(s)
* *V<sub>i</sub>*: 进样体积(ml)
* *V<sub>f</sub>*: 定容体积(ml)
* *D<sub>f</sub>*: 稀释倍数
* *m*: 称样质量(mg)
* *TE*: 传输效率 (需要计算后得到)


## 运行环境
* python: 3.8
* 依赖库：requirements.txt


## 同位素单位强度文件
* 同位素单位强度文件:mass_factor.csv (需求方提供)
* 同位素单位强度和embedding文件: isotopes_info.csv（计算得到）


## 配置样品质量配比文件：
* 配置样品质量配比文件：configuration_samples_mass.csv (需求方提供)


## 原始文件说明
* 标准样品: 197Au.csv
* 纯样品:meihui.csv, turang.csv, weiqi.csv
* 配置样品:s1.csv, s2.csv, s3.csv, s4.csv, s5.csv, s6.csv
* 真实样品:A1.csv, A3.csv, A5.csv


## 第一阶段
* particle_classify.py
* main_stage1.py
### 实现的功能：
* 颗粒态粒子筛选
* 颗粒态粒子的强度转质量，对颗粒添加embedding
* 计算TE（纯样品）
* 计算纳米颗粒数量（非纯样品）
* 计算单元素纳米颗粒数量（非纯样品）
### 入库的文件：
* 样品原始文件。例如：meihui.csv、 197Au.csv
* isotopes_info.csv
* TE(添加到机器&实验参数表中)
* 非标准样品的particle.csv
### 其他
* 纳米颗粒数量和单元素颗粒数量保存为number.csv，直接在前端展示即可，无需入库。


## 第二阶段
* fingerprint_analysis.py
* main_stage2.py
### 实现的功能：
* 频繁项的提取（纯样品，配置样品，真实样品都需要）
* 实现了对未知源的筛选
* 统计配置/真实样品频繁项目的统计信息，生成测试集和热力图文件
* 对纯样品建立分组，并提取指纹
* 得到分组中每种纯样品的指纹统计信息，生成训练集和热力图文件
* 得到该分组下纯样品单位质量的颗粒数(质量密度)，并计算配置样品中各种物质在该质量密度下的颗粒数占比
### 入库的文件：
* 配置/真实样品:
	* 频繁项文件 (support_0.01.csv)
	* 测试集（test.csv）
	* 热力图文件（HeatMap.csv）
* 纯样品：
	* 频繁项文件 (support_XXX.csv, 不在分组内)
	* 以下文件都在分组内：
		* 指纹文件 (fp_x.csv)
		* 热力图文件（HeatMap.csv）
		* 训练集（train.csv）
		* 配置样品数量比文件(configuration_samples_label.csv)


## 第三阶段
* trace_to_source.py
* main_stage3.py
### 实现的功能：
* 使用新分组中的训练集(纯样品)得到新版本模型
* 选择测试样品(配置/真实样品)进行溯源，要指定模型版本
* 模型包括：RF, SVM, XGBoost, GaussianNB
* 实现对unknown物质的识别
### 入库的文件：
* 要入库的文件都在分组内：
	* 该版本训练的模型文件（model.m）
	* 该版本使用的标准化参数文件(sc.bin)
	* 测试样品的溯源结果(trace_result.csv)

 ## 启动方法
 * 切换到particle环境
 * 输入uvicorn main:app --reload --port=

