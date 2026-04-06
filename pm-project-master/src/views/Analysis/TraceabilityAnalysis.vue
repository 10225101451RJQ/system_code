<template>
  <!-- 溯源 -->
  <div>
    <!-- 批次选择模块 -->
    <div>
      <el-row>
        <el-col :span=3>
          <el-button plain style="width: 95%" type="success"><b>{{ $t('Analysis.common.select.batch.label') }}</b>
          </el-button>
        </el-col>
        <el-col :span=6>
          <el-select v-model="batchInfo.batchId" :placeholder="$t('Analysis.common.select.batch.rule')" clearable>
            <el-option v-for="item in batchListStandard" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>
    <h4>
      {{
        $t('Analysis.AnalysisNotSource.analysis.functions.model.showString.str_1')
        + notSource_fp.bestModel.label
        + $t('Analysis.AnalysisNotSource.analysis.functions.model.showString.str_2')
      }}
    </h4>
    <div>
      <el-row>
        <el-form inline>
          <el-form-item :label="$t('Analysis.AnalysisNotSource.analysis.functions.traceResult.selectModel')">
            <el-cascader
                v-model="notSource_fp.selectModel"
                :options="notSource_fp.modelList"
                :placeholder="$t('Analysis.AnalysisNotSource.analysis.functions.model.rule_1')" clearable

                style="width: 300px"></el-cascader>
          </el-form-item>
          <el-button plain style="margin-left: 5px;margin-top: 5px" type="warning" size="small"
                     @click="updateBestModel">
            {{ $t('Analysis.AnalysisNotSource.analysis.btn.updateBestModel') }}
          </el-button>
        </el-form>
      </el-row>
      <el-row>
        <el-form inline>
          <el-form-item :label="$t('Sample.PostConfigSample.sampleProperty')" style="margin-right: 20px">
            <el-cascader ref="cascaderRefConfig" style="width: 300px"
                         @change="cascaderChangeConfig"
                         :placeholder="$t('Sample.PostConfigSample.selectFingerprintPlaceholder')"
                         :props="{checkStrictly: false, emitPath: false, multiple: true,}"
                         :value="casConfigList" :options="casConfigOpts" clearable/>
          </el-form-item>
          <el-form-item :label="$t('Sample.PostActualSample.sampleProperty')">
            <el-cascader ref="cascaderRefActual" style="width: 300px"
                         @change="cascaderChangeActual"
                         :placeholder="$t('Sample.PostActualSample.selectFingerprintPlaceholder')"
                         :props="{checkStrictly: false, emitPath: false, multiple: true,}"
                         :value="casActualList" :options="casActualOpts" clearable/>
          </el-form-item>
        </el-form>
        <div style="margin-top: -10px">
          <el-button plain type="primary" @click="testModelDefault">
            {{ $t('Analysis.AnalysisNotSource.analysis.btn.downloadTraceResult') }}
          </el-button>
          <el-button plain type="primary" :style="{display: btnShow}" @click="generateBarChart">
            {{ $t('Analysis.AnalysisNotSource.analysis.btn.generateBarChart') }}
          </el-button>
        </div>
      </el-row>
    </div>
    <el-tabs v-model="tabActiveName" style="margin-top: 30px" type="border-card">
      <el-tab-pane :label="$t('Analysis.common.chart.batChart')" name="BarChart">
        <BarChart></BarChart>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>

import BarChart from "../Chart/BarChart";
import {downloadCSV, postJSON} from "../../utils/api";

export default {
  name: "TraceabilityAnalysis",
  components: {BarChart},
  data() {
    return {
      // 级联选择相关
      casConfigList: [],
      casActualList: [],
      casConfigOpts: [],
      casActualOpts: [],
      // 批次相关
      btnShow: "none",
      batchListStandard: [],
      batchInfo: {
        batchId: "",
      },
      traceResultCSVUrl: '',
      tabActiveName: "BarChart",
      notSource_fp: {
        selectModel: [],
        modelList: [],
        bestModel: ""
      },
    }
  },
  mounted() {
    this.$bus.$on("updateModelList", this.getModelList)
  },
  async activated() {
    await postJSON('/batch/getBatchListStandard').then((resp) => {
      this.batchListStandard = resp.data.result.batchList
    })
  },
  watch: {
    'batchInfo.batchId': {
      handler() {
        this.notSource_fp = {
          selectModel: [],
          modelList: [],
          bestModel: ""
        }
        this.traceResultCSVUrl = ""
        this.btnShow = "none"
        if (this.batchInfo.batchId !== "") {
          // batchId变化且不为空时重新获取对应id的内容
          this.getSupportXList()
          this.getModelList()
        }
      }
    },
    'notSource_fp.selectModel': {
      handler() {
        this.traceResultCSVUrl = ""
        this.btnShow = "none"
      },
      deep: true
    },
    'casConfigList': {
      handler() {
        this.traceResultCSVUrl = ""
        this.btnShow = "none"
      },
      deep: true
    },
    'casActualList': {
      handler() {
        this.traceResultCSVUrl = ""
        this.btnShow = "none"
      },
      deep: true
    }
  },
  methods: {
    cascaderChangeConfig(value) {
      this.getValueConfig(this.casConfigList, 'cascaderRefConfig', value)
    },
    // 偷个懒后面再改QAQ
    cascaderChangeActual(value) {
      this.getValueActual(this.casActualList, 'cascaderRefActual', value)
    },
    getValueConfig(initVal, refName, value) {
      var nodes = this.$refs[refName].getCheckedNodes()
      if (nodes.length === 0) {
        this.casConfigList = []
        return
      }
      const editArray = []
      // 新增的值
      const newData = []
      const cancelData = []

      nodes.forEach(item => {
        const find = initVal.findIndex(id => id === item?.path[1] && item.checked) !== -1
        const findCancel = value.findIndex(id => id === item?.path[1] && item.checked) === -1

        if (findCancel || !item.checked) {
          cancelData.push({...item, checked: false})
        } else if (find) {
          // 已经选中的一级
          editArray.push({parent: item?.path[0], child: item?.path[1]})
        } else if (item.checked) {
          // 已经选择的新的
          newData.push(item)
        }
      })
      const lastNode = newData[newData.length - 1]
      // 最后操作的节点，首级存在在已经在的值内
      // 新点击的节点在同一父级下
      if (editArray.findIndex(i => i.parent === lastNode?.path?.[0]) !== -1) {
        const newBranch = this.casConfigList.filter(id => {
          return editArray.findIndex(i => i.child === id && lastNode?.path?.[0] === i.parent) === -1
        })
        newBranch.unshift(lastNode?.path?.[1])
        this.casConfigList = newBranch
      } else {  // 新点击的节点不在同一父级下
        const newBranch = this.casConfigList.filter(id => {
          return cancelData.findIndex(item => item.path[1] === id) === -1 && nodes.findIndex(item => item.path[1] === id) !== -1
        })
        if (lastNode?.path?.[1]) {
          newBranch.unshift(lastNode.path[1])
        }
        this.casConfigList = newBranch
      }
    },
    getValueActual(initVal, refName, value) {
      var nodes = this.$refs[refName].getCheckedNodes()
      if (nodes.length === 0) {
        this.casActualList = []
        return
      }
      const editArray = []
      // 新增的值
      const newData = []
      const cancelData = []

      nodes.forEach(item => {
        const find = initVal.findIndex(id => id === item?.path[1] && item.checked) !== -1
        const findCancel = value.findIndex(id => id === item?.path[1] && item.checked) === -1

        if (findCancel || !item.checked) {
          cancelData.push({...item, checked: false})
        } else if (find) {
          editArray.push({parent: item?.path[0], child: item?.path[1]})
        } else if (item.checked) {
          newData.push(item)
        }
      })
      const lastNode = newData[newData.length - 1]
      if (editArray.findIndex(i => i.parent === lastNode?.path?.[0]) !== -1) {
        const newBranch = this.casActualList.filter(id => {
          return editArray.findIndex(i => i.child === id && lastNode?.path?.[0] === i.parent) === -1
        })
        newBranch.unshift(lastNode?.path?.[1])
        this.casActualList = newBranch
      } else {
        const newBranch = this.casActualList.filter(id => {
          return cancelData.findIndex(item => item.path[1] === id) === -1 && nodes.findIndex(item => item.path[1] === id) !== -1
        })
        if (lastNode?.path?.[1]) {
          newBranch.unshift(lastNode.path[1])
        }
        this.casActualList = newBranch
      }
    },
    // 获取该批次下已经使用x生成的指纹文件
    getSupportXList() {
      postJSON('/batch/getSupportXList', {
        batchId: this.batchInfo.batchId
      }).then((resp) => {
        this.casConfigOpts = resp.data.result.sampleOpts.configSample
        this.casActualOpts = resp.data.result.sampleOpts.actualSample
      })
    },
    // 获取模型列表
    getModelList() {
      postJSON('/batch/getModelList', {
        batchId: this.batchInfo.batchId,
      }).then((resp) => {
        this.notSource_fp.modelList = resp.data.result.modelList
        this.notSource_fp.bestModel = resp.data.result.bestModel
      });
    },
    // 更新最优模型
    updateBestModel() {
      if (this.notSource_fp.selectModel.length === 0) {
        this.$message.warning(this.$t('Analysis.AnalysisNotSource.analysis.functions.model.rule_2'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/analysis/updateBestModel', {
        groupId: this.notSource_fp.selectModel[0],
        modelType: this.notSource_fp.selectModel[1]
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$message.success(resp.data.message)
          this.getModelList()
        } else this.$message.error(resp.data.message)
      });
    },
    // 生成柱状图
    generateBarChart() {
      this.tabActiveName = "BarChart"
      this.$bus.$emit("drawBarChart", {url: this.traceResultCSVUrl})
    },
    // 下载溯源文件
    testModelDefault() {
      if (this.batchInfo.batchId === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.noBatchSelect'))
        return
      }
      if (this.notSource_fp.bestModel === "") {
        this.$message.warning(this.$t('Analysis.AnalysisNotSource.analysis.functions.model.rule_3'))
        return
      }
      if (this.casConfigList.length === 0 && this.casActualList.length === 0) {
        this.$message.warning(this.$t('Analysis.AnalysisNotSource.analysis.functions.traceResult.rule_1'))
        return
      }
      if (this.notSource_fp.selectModel.length === 0) { // 如果不选择模型，使用默认模型分析
        this.$confirm(this.$t('Analysis.AnalysisNotSource.analysis.functions.model.rule_4'), this.$t('Common.confirm.title'), {
          confirmButtonText: this.$t('Common.confirm.btn.ok'),
          cancelButtonText: this.$t('Common.confirm.btn.cancel'),
          type: 'warning'
        }).then(() => {
          this.downloadTraceResult(true)
        }).catch(() => {
          this.$message({type: 'info', message: this.$t('Common.message.cancelText')})
        })
      } else this.downloadTraceResult(false)
    },
    downloadTraceResult(isModelDefault) {
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      postJSON('/download/traceResultCSV', {
        groupId: this.notSource_fp.selectModel[0],
        modelType: this.notSource_fp.selectModel[1],
        configSample: this.casConfigList.toString(),
        actualSample: this.casActualList.toString(),
        isModelDefault: isModelDefault,
        batchId: this.batchInfo.batchId
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$message.success(resp.data.message)
          this.traceResultCSVUrl = resp.data.result.url
          postJSON('/download/url', {url: this.traceResultCSVUrl}).then((resp) => {
            if (isModelDefault)
              downloadCSV(resp, this.$t("Analysis.AnalysisNotSource.analysis.functions.model.data") +
                  "-" + this.notSource_fp.bestModel.label)
            else downloadCSV(resp, this.$t("Analysis.AnalysisNotSource.analysis.functions.model.data") +
                "-" + this.notSource_fp.selectModel[0] + "_" + this.notSource_fp.selectModel[1])
          })
          if (this.casConfigList.length !== 0)
            this.btnShow = ''
        } else if (resp.data.code === 1) {
          this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
            confirmButtonText: this.$t('Common.confirm.btn.ok'),
            type: 'warning'
          })
        } else {
          this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
            confirmButtonText: this.$t('Common.confirm.btn.ok'),
            type: 'error'
          })
        }
      });
    },
  }
}
</script>

<style lang="less" scoped>
.hide {
  .el-cascader-menu:first-of-type {
    .el-cascader-node {
      .el-checkbox {
        display: none;
      }
    }
  }
}
</style>