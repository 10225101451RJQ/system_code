// 英文
export default {
    Common: {
        loading: {text: 'Executing, please wait a moment'},
        confirm: {
            title: 'Prompt',
            msg: {
                cancel: 'This operation will not be saved. Do you want to continue?',
                recycleBin: 'The files will be placed in the recycle bin and completely deleted after 30 days',
                recover: 'Confirm recovery?',
                delete: 'Irrevocable. Are you sure to completely delete it?',
            },
            btn: {ok: 'Yes', create: 'Create', cancel: 'Cancel', download: 'Download'},
        },
        message: {cancelText: 'Cancelled'},
        numRule: {
            empty: 'Enter content',
            num: 'Enter a number',
            over0: 'Enter a positive integer of 0 and above'
        }
    },
    CommonHeader: {
        title: 'Single Particle Metal Analysis Cloud',
        menu: {
            batch: 'Sample Information',
            analysis: 'Analysis'
        },
        dropdown: {
            usrInfo: 'User Info',
            logout: 'Log Out'
        }
    },
    CommonTableOperation: {
        operation: 'Operations'
    },
    Login: {
        title: 'Single Particle',
        title_2: 'Metal Analysis Cloud',
        introduction: 'Single-particle inductively coupled plasma time-of-flight mass spectrometry (SP-ICP-TOF-MS) data processing and visualization platform facilitates particle counting, fingerprint extraction, and source tracing of samples.',
        loginBtn: 'Login',
        toRegister_1: 'No account?',
        toRegister_2: 'Click to register',
        toRegister_3: 'Do you want to register?',
        getBackPasswd: 'Existing account, forgotten password?',
        form: {
            email: {
                label: 'Email',
                rule_1: 'Enter email',
                rule_2: 'Enter the correct email',
            },
            password: {
                label: 'Password',
                rule_1: 'Enter password',
                rule_2: 'The password length should not be less than 3 digits',
                rule_3: 'The password length must not exceed 20 digits',
            },
        },
    },
    Register: {
        title: 'Single Particle',
        title_2: 'Metal Analysis Cloud',
        introduction: 'Single-particle inductively coupled plasma time-of-flight mass spectrometry (SP-ICP-TOF-MS) data processing and visualization platform facilitates particle counting, fingerprint extraction, and source tracing of samples.',
        registerBtn: 'Register',
        toLogin_1: 'Existing account?',
        toLogin_2: 'Click to login',
        toLogin_3: 'Registration successful, do you want to return to login?',
        form: {
            email: {
                label: 'Email',
                rule_1: 'Enter email',
                rule_2: 'Enter the correct email',
            },
            password: {
                label: 'Password',
                newLabel: 'New password',
                rule_1: 'Enter password',
                rule_2: 'The password length must not be less than 3 digits',
                rule_3: 'The password length must not exceed 20 digits',
            },
            passwordConfirm: {
                label: 'Confirm',
                rule_1: 'Confirm the password',
                rule_2: 'The password length should not be less than 3 digits',
                rule_3: 'The password length must not exceed 20 digits',
                rule_4: 'Password cannot be empty',
                rule_5: 'Password not match',
            },
            name: {
                label: 'Username',
                rule_1: 'Enter username',
                rule_2: 'Username must not be less than 1 word',
                rule_3: 'Username must not exceed 20 words',
            },
            captcha: {
                label: 'Captcha',
                rule_1: 'Enter captcha',
                rule_2: 'The captcha should not be empty',
                rule_3: 'The captcha is wrong',
            }
        },
        captcha: {
            sending: 'Sending...',
            send: 'Send',
            alreadySend: 'Already send captcha',
            countdown: 'Countdown in progress, please request the captcha later',
        }
    },
    GetBackPasswd: {
        title: 'Single Particle',
        title_2: 'Metal Analysis Cloud',
        introduction: 'Single-particle inductively coupled plasma time-of-flight mass spectrometry (SP-ICP-TOF-MS) data processing and visualization platform facilitates particle counting, fingerprint extraction, and source tracing of samples.',
        subTitle: 'Retrieve password',
        registerBtn: 'Retrieve',
        toLogin_1: 'Existing account?',
        toLogin_2: 'Click to login',
        toLogin_3: 'Password retrieval successful, do you want to return to login?',
        form: {
            email: {
                label: 'Email',
                rule_1: 'Enter email',
                rule_2: 'Enter the correct email',
            },
            password: {
                label: 'Password',
                newLabel: 'New password',
                rule_1: 'Enter password',
                rule_2: 'The password length must not be less than 3 digits',
                rule_3: 'The password length must not exceed 20 digits',
            },
            passwordConfirm: {
                label: 'Confirm',
                rule_1: 'Confirm the password',
                rule_2: 'The password length should not be less than 3 digits',
                rule_3: 'The password length must not exceed 20 digits',
                rule_4: 'Password cannot be empty',
                rule_5: 'Password not match',
            },
            name: {
                label: 'Username',
                rule_1: 'Enter username',
                rule_2: 'Username must not be less than 1 word',
                rule_3: 'Username must not exceed 20 words',
            },
            captcha: {
                label: 'Captcha',
                rule_1: 'Enter captcha',
                rule_2: 'The captcha should not be empty',
                rule_3: 'The captcha is wrong',
            }
        },
        captcha: {
            sending: 'Sending...',
            send: 'Send',
            alreadySend: 'Already send captcha',
            countdown: 'Countdown in progress, please request the captcha later',
        }
    },
    Sample: {
        common: {
            batchName: 'Batch name',
            sampleState: {
                label: 'Sample state',
                solid: 'solid',
                liquid: 'liquid',
            },
            sampleProperty: 'Sample property',
            sampleType: {
                label: 'Sample type',
                rule: 'Select a sample type'
            },
            sampleFile: {
                label: 'Sample file',
                selectBtn: 'Select file',
                tip: 'Only CSV file',
                uploadBtn: 'Upload',
                rule: {
                    leastFile_1: 'Upload at least 1 file at a time',
                    exceedFile_1: 'Only 1 file can be uploaded at a time',
                    exceedFile_10: 'Upload up to 10 files at a time',
                    exceedFile_30: 'Upload up to 30 files at a time',
                    empty: 'Select a file'
                }
            },
            params: {
                Df: {label: 'Dilution factor', rule: 'Enter dilution factor'},
                Vf: {label: 'Final volume (mL)', rule: 'Unit: mL'},
                m: {label: 'Sample weight (mg)', rule: 'Unit: mg'},
            },
        },
        PostStandardSample: {
            title: 'Upload standard sample',
            sampleProperty: 'Standard sample',
            introduction: 'Standard nanoparticle samples with known particle number concentration, for testing transport efficiency (TE)',
        },
        PostSourceSample: {
            title: 'Upload source',
            sampleProperty: 'Source',
            introduction: 'Sample of known sources, for traceability analysis only',
        },
        PostConfigSample: {
            title: 'Upload mix',
            sampleProperty: 'Mix',
            selectFingerprintPlaceholder: 'Select fingerprint(s) of config sample',
            introduction: 'Sample mixed with different ratios of source samples, for traceability analysis only',
            sampleMgMl: 'Mass (mg) or volume (mL) of each Source'
        },
        PostActualSample: {
            title: 'Upload sample',
            sampleProperty: 'Sample',
            selectFingerprintPlaceholder: 'Select fingerprint(s) of sample',
        },
        PostBlankSample: {
            title: 'Upload blank sample',
            sampleProperty: 'Blank',
        }
    },
    Batch: {
        common: {
            analysisType: {iteration: 'iteration', poisson: 'poisson'},
            menu: {
                batchList: 'All Batches',
                postBatch: 'New Batch',
                recycleBin: 'Recycle Bin',
            }
        },
        BatchList: {
            search: {
                label: 'Search',
                type: 'Search type',
                options: {
                    batchName: 'Batch name',
                    authorName: 'User',
                    time: 'Time'
                },
                rule_1: 'Default batch name',
                rule_2: 'Key words',
                startDate: 'Start date',
                toDate: 'to',
                endDate: 'End date',
            },
            tableOperation: {
                options: {
                    batchName: 'Batch name',
                    sampleState: 'Sample state',
                    position: 'Sampling location',
                    authorName: 'User',
                    time: 'Time',
                },
                blueBtn: 'View'
            },
        },
        PostBatch: {
            basicInfo: {
                title: 'Sample information',
                batchName: {label: 'Batch name', rule: 'Enter a batch name'},
                position: {label: 'Sampling location', rule: 'Enter the sampling location'},
                sampleState: {label: 'Sample state', rule: 'Select the sample state',},
                analysisType: {label: 'Analysis type', rule: 'Select the analysis type',},
            },
            params: {
                title: 'Experimental parameters',
                Cp: {label: 'Std. Conc. (particles/mL)', rule: 'Unit: particles/mL'},
                CpBase: {label: 'Base', rule: 'Enter the base number'},
                CpExponent: {label: 'Exponent', rule: 'Enter the exponent number'},
                Vi: {label: 'Inlet Volume (mL)', rule: 'Unit: mL'},
                V: {label: 'Sample Flow Rate (mL/min)', rule: 'Unit: mL/min'},
                T: {label: 'Scan Time (s)', rule: 'Unit: s'},
            },
            sampleType: {
                title: 'Sample type',
                rule: 'Content cannot be empty',
                addBtn: 'Add',
                delBtn: 'Delete'
            },
            calibrationCurvesFile: {
                title: 'Calibration curves'
            },
            configurationSamplesMass: {
                title: 'Configuration samples mass'
            },
            TE: {
                title: 'TE',
                auto_calculation: 'auto calculated',
                manual_input: 'manual input',
            },
            uploadFile: 'Upload files'
        },
        DetailBatch: {
            title: 'Batch details',
            batchInfo: {
                batchName: 'Batch name',
                authorName: 'User',
                position: 'Sampling location',
                analysisType: 'Analysis type',
                sampleState: 'Sample state',
                TE: 'TE',
                Cp: 'Std. Conc.',
                V: 'Sample Flow Rate',
                T: 'Scan Time',
                Vi: 'Inlet Volume',
                particles_mL: 'particles/mL',
            },
            tableOperation: {
                options: {
                    sampleName: 'Sample name',
                    sourceMass: 'Source and mass',
                    support: 'Supporting',
                    supportXList: 'Generated supporting',
                    Df: 'Dilution factor',
                    Vf: 'Final volume (mL)',
                    m: 'Sample weight (mg)',
                },
            }
        },
        RecycleBin: {
            tableOperation: {
                options: {
                    batchName: 'Batch name',
                    authorName: 'User',
                    position: 'Sampling location',
                    time: 'Time',
                    remainingTime: 'Remaining time',
                },
                blueBtn: 'Recover'
            },
        }
    },
    Analysis: {
        common: {
            menu: {
                basicAnalysis: 'Basic',
                fingerpintAnalysis: 'Fingerprint',
                advancedAnalysis: 'Advanced',
                detectionLimitCalculation: 'Detection Limit Calculation',
                particle: 'Particle Analysis',
                supportX: 'Extract Fingerprint',
                analysisSource: 'Source Fingerprint',
                analysisNotSource: 'Sample Fingerprint',
                traceabilityAnalysis: 'Traceability Analysis',
                fingerprintDiffSame: 'Similarity-Difference Analysis',
            },
            select: {
                batch: {
                    label: 'Batch',
                    rule: 'Select a batch',
                },
                sampleProperty: {
                    label: 'Sample property',
                    rule: 'Select sample property'
                },
                msg: {
                    emptySelect: 'Select batch and sample information',
                    noBatchSelect: 'Select a batch',
                }
            },
            chart: {
                heatMap: 'Heat map',
                batChart: 'Hisotogram'
            },
            btn: {
                runAnalysis: 'Analysis',
                show: 'Show content',
                generate: 'Generate',
                download: 'Download file',
                downloadHeatMapData: 'Download data',
            }
        },
        DetectionLimitCalculation: {
            btn: {
                mass: 'Mass Detection Limit',
                particleConc: 'Particle Conc. Detection Limit',
            }
        },
        Particle: {
            btn: {
                particleCounts: 'Particle Counts',
                particleConc: 'Particle Conc.',
                dissolvedConc: 'Dissolved Conc.',
                particleMass: 'Particle Mass',
                massRatio: 'Mass Ratio',
                particleSize: 'Particle Size',
            }
        },
        SupportX: {
            support: {
                label: 'Supporting',
                rule_1: 'Enter supporting',
                rule_2: 'Enter a number in the range [0.001, 0.009] if Source',
                rule_3: 'Enter a number in the range (0, 1)'
            },
        },
        AnalysisSource: {
            createGroup: {
                title: 'Create group',
                support: {
                    rule: 'Select supporting'
                },
                logBase: {
                    label: 'Base number',
                    rule: 'Log base, default 10',
                    btn: 'Create'
                }
            },
            analysis: {
                title: 'Select group and analyze',
                subTitle: 'Analysis',
                group: {
                    showString: {
                        str_1: 'The group you are currently selecting is: ',
                        str_2: ', the log base is ',
                    },
                    rule: 'Select a group'
                },
                functions: {
                    fp: ' Fingerprint file',
                    train: 'Training',
                    sourceParticleConc: 'Source Particle Conc.',
                    sourceParticleContribution: 'Source Particle Contribution',
                    model: {
                        label: 'Generate model',
                        rule: 'Select a model type',
                    },
                },
                table: {
                    options: {
                        source: 'Source type and supporting',
                        logBase: 'Log base',
                        isModel: 'Generated models',
                    }
                },
            }
        },
        AnalysisNotSource: {
            sampleList: {
                title: 'Select sample',
                logBase: {
                    label: 'Base number',
                    rule: 'Log base, default 10',
                }
            },
            analysis: {
                subTitle: 'analysis',
                sample: {
                    showString: {
                        str_1: 'Your currently selected ',
                        str_2: ' is: ',
                        str_3: ' , supporting is: ',
                    },
                },
                functions: {
                    test: 'Testing fingerprint',
                    model: {
                        label: 'Model',
                        data: 'Trace result',
                        showString: {
                            str_1: 'The optimal model for the current batch is ',
                            str_2: ' , the optimal model is selected for analysis by default',
                        },
                        rule_1: 'Select the model type',
                        rule_2: 'No model selected, cannot update',
                        rule_3: 'Optimal model is empty, select a model and update it to the optimal model',
                        rule_4: 'The analysis will be performed using the global optimal model',
                    },
                    traceResult: {
                        selectModel: 'Select model',
                        rule_1: 'Select at least 1 fingerprint of not-source sample to trace result'
                    },
                },
                table: {
                    options: {
                        source: 'Source type and supporting',
                        logBase: 'Log base',
                        isModel: 'Generated models',
                    }
                },
                btn: {
                    downloadTraceResult: 'Generate and download results',
                    generateBarChart: 'Generate hisotogram',
                    updateBestModel: 'Update to optimal model',
                }
            }
        },
        FingerprintDiffSame: {
            uploadFiles: 'Upload files to be analyzed',
            allFingerprint: 'All fingerprint',
            specificFingerprint: 'Specific fingerprint',
            filteredElement: 'Input the elements to filter',
            addFilteredElement: '+ Add filtered element',
            tag: 'Upload test.csv files generated under 「Sample Fingerprint」 module for each sample to be analyzed',
            msg: {
                wrongElement: 'The input element is incorrect',
            },
            rule: {
                leastElement_1: 'Input at least one element'
            }
        },
    }
}