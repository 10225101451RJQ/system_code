<template>
  <!-- 检测限计算 -->
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
          <el-select v-model="detectionLimit.sampleProperty"
                     :placeholder="$t('Analysis.common.select.sampleProperty.rule')"
                     clearable>
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <common-table-single :table-data="detectionLimit.sampleList"
                           :table-label="detectionLimit.sampleLabel"
                           function="detectionLimit"
                           @change="resolveBug"></common-table-single>
      <!-- 执行分析 -->
      <el-button type="primary" @click="runDetectionLimit()">{{ $t('Analysis.common.btn.runAnalysis') }}</el-button>
      <!-- 质量检测限 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('mass')">
        {{ $t('Analysis.DetectionLimitCalculation.btn.mass') }}
      </el-button>
      <!-- 数浓度检测限 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('particleConc')">
        {{ $t('Analysis.DetectionLimitCalculation.btn.particleConc') }}
      </el-button>
    </div>
  </div>
</template>

<script>
import {downloadCSV, postJSON} from "../../utils/api";
import CommonTableSingle from "../../components/CommonTableSingle";

export default {
  components: {CommonTableSingle},
  name: "DetectionLimitCalculation",
  data() {
    return {
      contentShow: "none",
      btnShow: 'none',
      batchListStandard: [],
      batchInfo: {
        batchId: "",
        sampleState: "",
        sampleList: [],
      },
      urls: "",
      detectionLimit: {
        sampleProperty: "",
        sampleList: [],
        sampleLabel: [],
        sampleId: "",   // 选中的样品id
        selectRow: ""
      },
      options: [
        {value: '空白样品', label: this.$t('Sample.PostBlankSample.sampleProperty')}
      ],
      tableLabel: {
        solid_blank: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        liquid_blank: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
      }
    }
  },
  mounted() {
    this.$bus.$on('returnSampleIdSingle', (data) => {
      if (data.function === 'detectionLimit') {
        this.detectionLimit.sampleId = data.sample.id;
        this.detectionLimit.selectRow = data.sample;
      }
    })
  },
  async activated() {
    await postJSON('/batch/getBatchListStandard').then((resp) => {
      this.batchListStandard = resp.data.result.batchList
    })
  },
  watch: {
    'detectionLimit.selectRow': {
      handler() {
        this.btnShow = 'none'
      }
    },
    'batchInfo.batchId': {
      handler() {
        // 清空所有用户输入内容
        this.detectionLimit = {
          sampleProperty: "",
          sampleList: [],
          sampleLabel: [],
          sampleId: "",   // 选中的样品id
          selectRow: ""
        }
        this.batchInfo.sampleList = []
        this.batchInfo.sampleState = ""
        this.urls = ""
        // batchId为空时清空所有用户输入内容
        if (this.batchInfo.batchId === "") {
          this.contentShow = "none"
        } else {
          this.contentShow = ""
          // batchId变化且不为空时重新获取对应id的内容
          this.getBatchInfo()
        }
      }
    },
    'detectionLimit.sampleProperty': {
      handler() {
        this.detectionLimit.sampleId = ""
        this.detectionLimit.selectRow = ""
        this.urls = ""
        if (this.detectionLimit.sampleProperty === "空白样品") {
          this.detectionLimit.sampleList = this.batchInfo.sampleList.blankSampleList;
          this.detectionLimit.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_blank : this.tableLabel.liquid_blank
        } else {
          this.detectionLimit.sampleList = []
          this.detectionLimit.sampleLabel = []
        }
      }
    },
  },
  methods: {
    getBatchInfo() {
      // 获取某一批次信息
      if (this.batchInfo.batchId === "") {
        this.$message.error(this.$t('Analysis.common.select.batch.rule'))
        return
      }
      postJSON('/batch/getBatchInfo', {batchId: this.batchInfo.batchId}).then((resp) => {
        if (resp.data.code === 0) {
          this.batchInfo.sampleState = resp.data.result.batchInfo.sampleState
          this.batchInfo.sampleList = resp.data.result.sampleList
          this.$message.success(resp.data.message)
        } else this.$message.warning(resp.data.message)
      });
    },
    // 颗粒态分析
    runDetectionLimit() {
      if (this.detectionLimit.sampleId === "" || this.detectionLimit.sampleProperty === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/analysis/detectionLimit', {
        sampleId: this.detectionLimit.sampleId,
        sampleProperty: this.detectionLimit.sampleProperty,
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.urls = resp.data.result.urls
          this.btnShow = ''
          this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
            confirmButtonText: this.$t('Common.confirm.btn.ok'),
            cancelButtonText: this.$t('Common.confirm.btn.cancel'),
            type: 'success'
          })
        } else if (resp.data.code === 1) {
          this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
            confirmButtonText: this.$t('Common.confirm.btn.ok'),
            cancelButtonText: this.$t('Common.confirm.btn.cancel'),
            type: 'warning'
          })
        } else {
          this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
            confirmButtonText: this.$t('Common.confirm.btn.ok'),
            cancelButtonText: this.$t('Common.confirm.btn.cancel'),
            type: 'error'
          })
        }
      });
    },
    // 检测限计算
    downloadFile(fileName) {
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      let name = ''
      if (fileName === 'mass')
        name = this.$t('Analysis.DetectionLimitCalculation.btn.mass')
      else if (fileName === 'particleConc')
        name = this.$t('Analysis.DetectionLimitCalculation.btn.particleConc')
      postJSON('/download/url', {url: this.urls[fileName]}).then((resp) => {
        loading.close();
        downloadCSV(resp, name)
      });
    },
    resolveBug() {
      this.$forceUpdate();
    }
  }
}
</script>

<style lang="less" scoped>
</style>