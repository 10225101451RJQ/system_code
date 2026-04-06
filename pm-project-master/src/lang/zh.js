// 中文
export default {
    Common: {
        loading: {text: '执行中，请稍等'},
        confirm: {
            title: '提示',
            msg: {
                cancel: '此操作将不会保存, 是否继续？',
                recover: '确认恢复吗？',
                recycleBin: '文件将放入回收站，30天后彻底删除',
                delete: '不可撤销，确认彻底删除吗？',
            },
            btn: {ok: '确定', create: '新建', cancel: '取消', download: '下载'},
        },
        message: {cancelText: '已取消'},
        numRule: {
            empty: '请输入内容',
            num: '请输入数字',
            over0: '请输入0及0以上正整数'
        }
    },
    CommonHeader: {
        title: '单颗粒金属全元素分析云',
        menu: {
            batch: '样品信息',
            analysis: '样品分析'
        },
        dropdown: {
            usrInfo: '用户信息',
            logout: '退出'
        }
    },
    CommonTableOperation: {
        operation: '操作'
    },
    Login: {
        title: '单颗粒金属全元素分析云',
        title_2: '',
        introduction: '单颗粒飞行时间质谱仪（SP-ICP-TOF-MS）数据处理及可视化平台，助力快速实现样品颗粒计数、指纹提取、建模溯源等全流程分析。',
        loginBtn: '登录',
        toRegister_1: '没有账号？',
        toRegister_2: '点击注册',
        toRegister_3: '是否前往注册？',
        getBackPasswd: '已有帐号，忘记密码？',
        form: {
            email: {
                label: '电子邮箱',
                rule_1: '请输入电子邮箱',
                rule_2: '请输入正确的电子邮箱',
            },
            password: {
                label: '密码',
                rule_1: '请输入密码',
                rule_2: '密码长度不得少于3位',
                rule_3: '密码长度不得多于20位',
            },
        },
    },
    Register: {
        title: '单颗粒金属全元素分析云',
        title_2: '',
        introduction: '单颗粒飞行时间质谱仪（SP-ICP-TOF-MS）数据处理及可视化平台，助力快速实现样品颗粒计数、指纹提取、建模溯源等全流程分析。',
        registerBtn: '注册',
        toLogin_1: '已有账号？',
        toLogin_2: '点击登录',
        toLogin_3: '注册成功，是否返回登录？',
        form: {
            email: {
                label: '电子邮箱',
                rule_1: '请输入电子邮箱',
                rule_2: '请输入正确的电子邮箱',
            },
            password: {
                label: '密码',
                newLabel: '新密码',
                rule_1: '请输入密码',
                rule_2: '密码长度不得少于3位',
                rule_3: '密码长度不得多于20位',
            },
            passwordConfirm: {
                label: '确认密码',
                rule_1: '请确认密码',
                rule_2: '密码长度不得少于3位',
                rule_3: '密码长度不得多于20位',
                rule_4: '密码不得为空',
                rule_5: '密码不符',
            },
            name: {
                label: '用户名',
                rule_1: '请输入用户名',
                rule_2: '用户名不得少于1个字',
                rule_3: '用户名不得多于20个字',
            },
            captcha: {
                label: '验证码',
                rule_1: '请输入验证码',
                rule_2: '验证码不得为空',
                rule_3: '验证码有误',
            },
        },
        captcha: {
            sending: '发送中...',
            send: '发送',
            alreadySend: '已发送验证码',
            countdown: '倒计时中，请稍后再请求验证码',
        }
    },
    GetBackPasswd: {
        title: '单颗粒金属全元素分析云',
        title_2: '',
        introduction: '单颗粒飞行时间质谱仪（SP-ICP-TOF-MS）数据处理及可视化平台，助力快速实现样品颗粒计数、指纹提取、建模溯源等全流程分析。',
        subTitle: '找回密码',
        registerBtn: '找回',
        toLogin_1: '已有账号？',
        toLogin_2: '点击登录',
        toLogin_3: '找回密码成功，是否返回登录？',
        form: {
            email: {
                label: '电子邮箱',
                rule_1: '请输入电子邮箱',
                rule_2: '请输入正确的电子邮箱',
            },
            password: {
                label: '密码',
                newLabel: '新密码',
                rule_1: '请输入密码',
                rule_2: '密码长度不得少于3位',
                rule_3: '密码长度不得多于20位',
            },
            passwordConfirm: {
                label: '确认密码',
                rule_1: '请确认密码',
                rule_2: '密码长度不得少于3位',
                rule_3: '密码长度不得多于20位',
                rule_4: '密码不得为空',
                rule_5: '密码不符',
            },
            name: {
                label: '用户名',
                rule_1: '请输入用户名',
                rule_2: '用户名不得少于1个字',
                rule_3: '用户名不得多于20个字',
            },
            captcha: {
                label: '验证码',
                rule_1: '请输入验证码',
                rule_2: '验证码不得为空',
                rule_3: '验证码有误',
            },
        },
        captcha: {
            sending: '发送中...',
            send: '发送',
            alreadySend: '已发送验证码',
            countdown: '倒计时中，请稍后再请求验证码',
        }
    },
    Sample: {
        common: {
            batchName: '批次名称',
            sampleState: {
                label: '样品形态',
                solid: '固体',
                liquid: '液体',
            },
            sampleProperty: '样品属性',
            sampleType: {
                label: '样品类型',
                rule: '请选择样品类型'
            },
            sampleFile: {
                label: '样品文件',
                selectBtn: '选取文件',
                tip: '只能上传csv文件',
                uploadBtn: '上传',
                rule: {
                    leastFile_1: '一次至少上传1个文件',
                    exceedFile_1: '一次只允许上传1个文件',
                    exceedFile_10: '一次最多上传10个文件',
                    exceedFile_30: '一次最多上传30个文件',
                    empty: '请选择文件'
                }
            },
            params: {
                Df: {label: '稀释倍数', rule: '请输入稀释倍数'},
                Vf: {label: '定容体积 (mL)', rule: '单位：mL'},
                m: {label: '称样质量 (mg)', rule: '单位：mg'},
            },
        },
        PostStandardSample: {
            title: '上传标准样品',
            sampleProperty: '标准样品',
            introduction: '已知颗粒数浓度的纳米颗粒标准样品，用于测试传输效率（TE）',
        },
        PostSourceSample: {
            title: '上传源样品',
            sampleProperty: '源样品',
            introduction: '已知来源的样品，仅用于溯源分析',
        },
        PostConfigSample: {
            title: '上传配置样品',
            sampleProperty: '配置样品',
            selectFingerprintPlaceholder: '请选择配置样品指纹',
            introduction: '各源样品按不同比例配置的样品，仅用于溯源分析',
            sampleMgMl: '每种源样品的质量（mg）或体积（mL）'
        },
        PostActualSample: {
            title: '上传样品',
            sampleProperty: '样品',
            selectFingerprintPlaceholder: '请选择样品指纹',
        },
        PostBlankSample: {
            title: '上传空白样品',
            sampleProperty: '空白样品',
        }
    },
    Batch: {
        common: {
            analysisType: {iteration: '迭代法', poisson: '泊松法'},
            menu: {
                batchList: '全部批次',
                postBatch: '新建批次',
                recycleBin: '回收站',
            }
        },
        BatchList: {
            search: {
                label: '搜索',
                type: '搜索方式',
                options: {
                    batchName: '按批次名',
                    authorName: '按创建人',
                    time: '按创建时间'
                },
                rule_1: '默认以批次名搜索',
                rule_2: '请输入搜索内容',
                startDate: '开始日期',
                toDate: '至',
                endDate: '结束日期',
            },
            tableOperation: {
                options: {
                    batchName: '批次名',
                    sampleState: '样品形态',
                    position: '采样地点',
                    authorName: '创建人',
                    time: '创建时间',
                },
                blueBtn: '查看'
            },
        },
        PostBatch: {
            basicInfo: {
                title: '基本信息',
                batchName: {label: '批次名', rule: '请输入批次名'},
                position: {label: '采样地点', rule: '请输入采样地点'},
                sampleState: {label: '样品形态', rule: '请选择样品形态',},
                analysisType: {label: '分析类型', rule: '请选择分析类型',},
            },
            params: {
                title: '实验参数',
                Cp: {label: '标样数浓度（个/mL)', rule: '单位：个/mL'},
                CpBase: {label: '底数', rule: '请输入底数'},
                CpExponent: {label: '指数', rule: '请输入指数'},
                Vi: {label: '进样体积 (mL)', rule: '单位：mL'},
                V: {label: '进样流速 (mL/min)', rule: '单位：mL/min'},
                T: {label: '测试时间 (s)', rule: '单位：s'},
            },
            sampleType: {
                title: '样品类型',
                rule: '内容不能为空',
                addBtn: '增加',
                delBtn: '删除'
            },
            calibrationCurvesFile: {
                title: '元素标准曲线'
            },
            configurationSamplesMass: {
                title: '配置样品质量配比'
            },
            TE: {
                title: 'TE',
                auto_calculation: '自动计算',
                manual_input: '手动输入',
            },
            uploadFile: '文件上传'
        },
        DetailBatch: {
            title: '批次详情',
            batchInfo: {
                batchName: '批次名',
                authorName: '创建人',
                position: '采样地点',
                analysisType: '分析类型',
                sampleState: '样品形态',
                TE: '传输效率 TE',
                Cp: '数浓度',
                V: '流速',
                T: '测试时间',
                Vi: '进样体积',
                particles_mL: '个/mL',
            },
            tableOperation: {
                options: {
                    sampleName: '样品名称',
                    sourceMass: '配置样品物质及质量',
                    support: '支持度',
                    supportXList: '已生成的支持度',
                    Df: '稀释倍数',
                    Vf: '定容体积 (mL)',
                    m: '称样质量 (mg)',
                },
            }
        },
        RecycleBin: {
            tableOperation: {
                options: {
                    batchName: '批次名',
                    authorName: '创建人',
                    position: '采样地点',
                    time: '创建时间',
                    remainingTime: '剩余时间',
                },
                blueBtn: '恢复'
            },
        }
    },
    Analysis: {
        common: {
            menu: {
                basicAnalysis: '基础分析',
                fingerpintAnalysis: '指纹分析',
                advancedAnalysis: '进阶分析',
                detectionLimitCalculation: '检测限计算',
                particle: '颗粒态分析',
                supportX: '指纹提取',
                analysisSource: '源样品指纹',
                analysisNotSource: '样品指纹',
                traceabilityAnalysis: '溯源分析',
                fingerprintDiffSame: '指纹异同分析',
            },
            select: {
                batch: {
                    label: '批次',
                    rule: '请选择批次',
                },
                sampleProperty: {
                    label: '样品属性',
                    rule: '请选择样品属性'
                },
                msg: {
                    emptySelect: '请选择批次和样品',
                    noBatchSelect: '请选择批次',
                }
            },
            chart: {
                heatMap: '热力图',
                batChart: '柱状图'
            },
            btn: {
                runAnalysis: '执行分析',
                show: '显示内容',
                generate: '生成',
                download: '下载文件',
                downloadHeatMapData: '下载热力图数据',
            }
        },
        DetectionLimitCalculation: {
            btn: {
                mass: '质量检测限',
                particleConc: '颗粒态数浓度检测限',
            }
        },
        Particle: {
            btn: {
                particleCounts: '单颗粒计数',
                particleConc: '颗粒态数浓度',
                dissolvedConc: '溶解态浓度',
                particleMass: '单颗粒元素质量',
                massRatio: '单颗粒元素质量占比',
                particleSize: '颗粒粒径',
            }
        },
        SupportX: {
            support: {
                label: '支持度',
                rule_1: '请输入支持度',
                rule_2: '源样品请输入范围[0.001, 0.009]内数字',
                rule_3: '请输入范围(0, 1)内数字'
            },
        },
        AnalysisSource: {
            createGroup: {
                title: '创建分组',
                support: {
                    rule: '请选择支持度'
                },
                logBase: {
                    label: '底数',
                    rule: '请输入log底数，默认为10',
                    btn: '生成分组'
                }
            },
            analysis: {
                title: '选择分组并分析',
                subTitle: '分析功能',
                group: {
                    showString: {
                        str_1: '您当前选择的分组是：',
                        str_2: '，log底数为',
                    },
                    rule: '请选择分组'
                },
                functions: {
                    fp: '指纹文件',
                    train: '训练集',
                    sourceParticleConc: '源样品颗粒数浓度',
                    sourceParticleContribution: '各源样品颗粒数贡献',
                    model: {
                        label: '生成模型',
                        rule: '请选择模型类型',
                    },
                },
                table: {
                    options: {
                        source: '样品类型及支持度',
                        logBase: 'log底数',
                        isModel: '是否生成了模型',
                    }
                },
            }
        },
        AnalysisNotSource: {
            sampleList: {
                title: '选择样品',
                logBase: {
                    label: '底数',
                    rule: '请输入log底数，默认为10',
                }
            },
            analysis: {
                subTitle: '分析功能',
                sample: {
                    showString: {
                        str_1: '您当前选择的',
                        str_2: '是：',
                        str_3: '，支持度为：',
                    },
                },
                functions: {
                    test: '指纹信息文件（测试集）',
                    model: {
                        label: '溯源模型',
                        data: '溯源结果',
                        showString: {
                            str_1: '当前批次最优模型为',
                            str_2: '，默认选择最优模型分析',
                        },
                        rule_1: '请选择模型类型',
                        rule_2: '未选择模型，无法更新',
                        rule_3: '最优模型为空，请选择一个模型并更新其为最优模型',
                        rule_4: '将使用全局最优模型进行分析',
                    },
                    traceResult: {
                        selectModel: '选择模型',
                        rule_1: '请选择至少一个非源样品指纹进行溯源'
                    },
                },
                table: {
                    options: {
                        source: '样品类型及支持度',
                        logBase: 'log底数',
                        isModel: '是否生成了模型',
                    }
                },
                btn: {
                    downloadTraceResult: '生成并下载溯源结果',
                    generateBarChart: '生成柱状图',
                    updateBestModel: '更新其为最优模型',
                }
            }
        },
        FingerprintDiffSame: {
            uploadFiles: '上传待分析的文件',
            allFingerprint: '所有指纹',
            specificFingerprint: '特定指纹',
            filteredElement: '选择需要筛选的元素',
            addFilteredElement: '+ 添加筛选元素',
            tag: '请上传待分析的各样品在「样品指纹」模块下生成的test.csv文件',
            msg: {
                wrongElement: '输入的元素有误',
            },
            rule: {
                leastElement_1: '至少输入一个元素'
            }
        },
    }
}