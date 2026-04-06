<template>
  <!-- 样品指纹分析 -->
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
    <!-- 动态展示模块 -->
    <div :style="{'margin-top':'10px','margin-bottom':'10px'}">
      <el-row>
        <el-col :span=3>
          <el-button plain style="width: 95%" type="success">
            <b>{{ $t('Analysis.common.select.sampleProperty.label') }}</b></el-button>
        </el-col>
        <el-col :span=6>
          <el-select v-model="notSource_fp.sampleProperty"
                     :placeholder="$t('Analysis.common.select.sampleProperty.rule')"
                     clearable>
            <el-option v-for="item in samplePropertyOptions" :key="item.value" :label="item.label"
                       :value="item.value">
            </el-option>
          </el-select>
        </el-col>
      </el-row>
      <h4>{{ $t('Analysis.AnalysisNotSource.sampleList.title') }}</h4>
      <common-table-single :table-data="notSource_fp.xSampleList"
                           :table-label="notSource_fp.xSampleLabel"
                           function="notSource"></common-table-single>
      <h5>{{ show.sampleString }}</h5>
      <el-form ref="logBaseForm" :inline="true" :model="notSource_fp" :rules="rules" label-width="120px"
               style="margin-top: 10px">
        <el-form-item label-width="120px" :label="$t('Analysis.AnalysisNotSource.sampleList.logBase.label')"
                      prop="logBase">
          <el-input v-model="notSource_fp.logBase"
                    :placeholder="$t('Analysis.AnalysisNotSource.sampleList.logBase.rule')"
                    class="input-box"></el-input>
        </el-form-item>
      </el-form>
      <el-descriptions :column="2" :title="$t('Analysis.AnalysisNotSource.analysis.subTitle')" border>
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.AnalysisNotSource.analysis.functions.test') }}</template>
          <el-button plain size="small" type="primary" @click="generateTestCSV">
            {{ $t('Analysis.common.btn.generate') }}
          </el-button>
          <el-button plain size="small" type="primary" @click="downloadTestCSV">
            {{ $t('Analysis.common.btn.download') }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.common.chart.heatMap') }}</template>
          <el-button plain size="small" style="margin-left: 10px" type="primary" @click="generateHeatMap">
            {{ $t('Analysis.common.btn.generate') }}
          </el-button>
          <el-button plain size="small" style="margin-left: 10px" type="primary" @click="downloadHeatMapData">
            {{ $t('Analysis.common.btn.downloadHeatMapData') }}
          </el-button>
        </el-descriptions-item>
      </el-descriptions>
      <el-tabs v-model="tabActiveName" style="margin-top: 10px" type="border-card">
        <el-tab-pane :label="$t('Analysis.common.chart.heatMap')" name="HeatMap">
          <HeatMapNotSource :heat-map-info="heatMapInfo" heat-map-id="heatMapNotSource"></HeatMapNotSource>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import CommonTableSingle from "../../components/CommonTableSingle";
import HeatMapNotSource from "../Chart/HeatMap";
import {downloadCSV, postJSON} from "../../utils/api";

export default {
  name: "AnalysisNotSource",
  components: {CommonTableSingle, HeatMapNotSource},
  data() {
    //包含小数的数字
    let valiNumDotPass = (rule, value, callback) => {
      let reg = /^[+-]?(0|([1-9]\d*))(\.\d+)?$/g;
      if (value === '') {
        callback(new Error(this.$t('Common.numRule.empty')));
      } else if (!reg.test(value)) {
        callback(new Error(this.$t('Common.numRule.num')));
      } else {
        callback();
      }
    };
    //正整数
    var valiNumPositivePass = (rule, value, callback) => {
      let reg = /^[+]{0,1}(\d+)$/g;
      if (value === '') {
        callback(new Error(this.$t('Common.numRule.empty')));
      } else if (!reg.test(value)) {
        callback(new Error(this.$t('Common.numRule.over0')));
      } else {
        callback();
      }
    };
    return {
      // 批次相关
      btnShow: "none",
      batchListStandard: [],
      batchInfo: {
        batchId: "",
        sampleState: "",
        sampleList: {},
        xSampleList: {}
      },
      tabActiveName: "HeatMap",
      heatMapInfo: "",
      notSource_fp: {
        logBase: "",
        sampleProperty: "",
        xSampleList: [],
        xSampleLabel: [],
        fileId: "",   // 选中的supportX文件id
        selectRow: "",
      },
      samplePropertyOptions: [
        {value: '配置样品', label: this.$t('Sample.PostConfigSample.sampleProperty')},
        {value: '样品', label: this.$t('Sample.PostActualSample.sampleProperty')},
      ],
      rules: {
        logBase: [{required: true, validator: valiNumDotPass, trigger: "blur"}],
      },
      tableLabel: {
        supportX_solid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "support", label: this.$t('Batch.DetailBatch.tableOperation.options.support')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        supportX_solid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "support", label: this.$t('Batch.DetailBatch.tableOperation.options.support')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        supportX_liquid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "support", label: this.$t('Batch.DetailBatch.tableOperation.options.support')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
        supportX_liquid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "support", label: this.$t('Batch.DetailBatch.tableOperation.options.support')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
      },
      show: {
        sampleString: ""
      }
    }
  },
  mounted() {
    this.$bus.$on('returnSampleIdSingle', (data) => {
      if (data.function === 'notSource') {
        this.notSource_fp.fileId = data.sample.fileId;
        this.notSource_fp.selectRow = data.sample;
      }
    })
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
          logBase: "",
          sampleProperty: "",
          xSampleList: [],
          xSampleLabel: [],
          fileId: "",   // 选中的supportX文件id
          selectRow: "",
        }
        this.btnShow = "none"
        this.batchInfo.sampleList = []
        this.batchInfo.sampleState = ""
        this.show.sampleString = ""
        if (this.batchInfo.batchId !== "") {
          // batchId变化且不为空时重新获取对应id的内容
          this.getBatchInfo()
        }
      }
    },
    'notSource_fp.sampleProperty': {
      handler() {
        this.notSource_fp.fileId = ""
        this.notSource_fp.selectRow = ""
        if (this.notSource_fp.sampleProperty === "配置样品") {
          this.notSource_fp.xSampleList = this.batchInfo.xSampleList.configSampleList
          this.notSource_fp.xSampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.supportX_solid_config : this.tableLabel.supportX_liquid_config
        } else if (this.notSource_fp.sampleProperty === "样品") {
          this.notSource_fp.xSampleList = this.batchInfo.xSampleList.actualSampleList
          this.notSource_fp.xSampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.supportX_solid_normal : this.tableLabel.supportX_liquid_normal
        } else {
          this.notSource_fp.xSampleList = []
          this.notSource_fp.xSampleLabel = []
        }
      }
    },
    'notSource_fp.selectRow': {
      handler() {
        if (this.notSource_fp.selectRow === "")
          this.show.sampleString = ""
        else this.show.sampleString = this.$t('Analysis.AnalysisNotSource.analysis.sample.showString.str_1') + this.notSource_fp.sampleProperty +
            this.$t('Analysis.AnalysisNotSource.analysis.sample.showString.str_2') + this.notSource_fp.selectRow.sampleName +
            this.$t('Analysis.AnalysisNotSource.analysis.sample.showString.str_3') + this.notSource_fp.selectRow.support
      }
    },
  },
  methods: {
    // 获取某一批次信息
    async getBatchInfo() {
      if (this.batchInfo.batchId === "") {
        this.$message.error(this.$t('Analysis.common.select.batch.rule'))
        return
      }
      await postJSON('/batch/getBatchInfo', {batchId: this.batchInfo.batchId}).then((resp) => {
        if (resp.data.code === 0) {
          this.batchInfo.sampleState = resp.data.result.batchInfo.sampleState
          this.batchInfo.sampleList = resp.data.result.sampleList
          this.$message.success(resp.data.message)
        } else {
          this.$message.warning(resp.data.message)
        }
      })
      this.getSupportXList()
    },
    // 获取该批次下已经使用x生成的指纹文件
    getSupportXList() {
      postJSON('/batch/getSupportXList', {
        batchId: this.batchInfo.batchId
      }).then((resp) => {
        this.batchInfo.xSampleList = resp.data.result.sampleList
      })
    },
    // 非纯物质，在该x下生成并下载test.csv文件
    async generateTestCSV() {
      if (this.notSource_fp.fileId === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      await this.$refs.logBaseForm.validate((valid) => {
        if (valid) {
          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postJSON('/analysis/generateTestCSV', {
            fileId: this.notSource_fp.fileId,
            sampleProperty: this.notSource_fp.sampleProperty,
            logBase: this.notSource_fp.logBase,
          }).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              this.$message.success(resp.data.message)
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
        } else {
          return false
        }
      })
    },
    downloadTestCSV() {
      if (this.notSource_fp.fileId === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      this.$refs.logBaseForm.validate((valid) => {
        if (valid) {
          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postJSON('/fileExist/testCSV', {
            fileId: this.notSource_fp.fileId,
            sampleProperty: this.notSource_fp.sampleProperty,
            logBase: this.notSource_fp.logBase,
          }).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              this.$message.success(resp.data.message)
              postJSON('/download/testCSV', {
                fileId: this.notSource_fp.fileId,
                sampleProperty: this.notSource_fp.sampleProperty,
                logBase: this.notSource_fp.logBase,
              }).then((resp) => {
                downloadCSV(resp, this.$t("Analysis.AnalysisNotSource.analysis.functions.test") + "-" +
                    this.notSource_fp.sampleProperty + "_" +
                    this.notSource_fp.selectRow.sampleName + "_" +
                    this.notSource_fp.selectRow.support +
                    this.notSource_fp.logBase)
              });
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
        } else return false;
      })
    },
    // 生成热力图
    generateHeatMap() {
      if (this.notSource_fp.fileId === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      this.$refs.logBaseForm.validate((valid) => {
        if (valid) {
          this.tabActiveName = "HeatMap"
          this.heatMapInfo = {
            type: 'notSource',
            groupId: "",
            fileId: this.notSource_fp.fileId,
            heatMapType: "",
            logBase: this.notSource_fp.logBase
          }
        } else return false;
      })
    },
    // 下载热力图数据文件
    downloadHeatMapData() {
      if (this.notSource_fp.fileId === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      this.$refs.logBaseForm.validate((valid) => {
        if (valid) {
          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postJSON('/fileExist/heatMapDataCSV', {
            id: this.notSource_fp.fileId,
            sampleProperty: "notSource",
            sampleType: "",
            logBase: this.notSource_fp.logBase
          }).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              this.$message.success(resp.data.message)
              postJSON('/download/heatMapDataCSV', {
                id: this.notSource_fp.fileId,
                sampleProperty: "notSource",
                sampleType: "",
                logBase: this.notSource_fp.logBase
              }).then((resp) => {
                downloadCSV(resp, this.$t("Analysis.common.chart.heatMap") + "-" +
                    this.notSource_fp.sampleProperty + "_" + this.notSource_fp.logBase)
              });
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
        } else return false;
      })
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