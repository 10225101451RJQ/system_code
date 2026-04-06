<template>
  <!-- 颗粒态分析 -->
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
          <el-select v-model="particle.sampleProperty" :placeholder="$t('Analysis.common.select.sampleProperty.rule')"
                     clearable>
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <common-table-single :table-data="particle.sampleList"
                           :table-label="particle.sampleLabel"
                           function="particle"
                           @change="resolveBug"></common-table-single>
      <!-- 执行分析 -->
      <el-button type="primary" @click="runParticle()">{{ $t('Analysis.common.btn.runAnalysis') }}</el-button>
      <!-- 单颗粒计数 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('particleCounts')">
        {{ $t('Analysis.Particle.btn.particleCounts') }}
      </el-button>
      <!-- 颗粒态数浓度 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('particleConc')">
        {{ $t('Analysis.Particle.btn.particleConc') }}
      </el-button>
      <!-- 溶解态浓度 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('dissolvedConc')">
        {{ $t('Analysis.Particle.btn.dissolvedConc') }}
      </el-button>
      <!-- 单颗粒元素质量 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('particleMass')">
        {{ $t('Analysis.Particle.btn.particleMass') }}
      </el-button>
      <!-- 单颗粒元素质量占比 -->
      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('massRatio')">
        {{ $t('Analysis.Particle.btn.massRatio') }}
      </el-button>
      <!-- 颗粒粒径 -->
<!--      <el-button :style="{display:btnShow}" plain type="primary" @click="downloadFile('particleSize')">-->
<!--        {{ $t('Analysis.Particle.btn.particleSize') }}-->
<!--      </el-button>-->
    </div>
  </div>
</template>

<script>
import {downloadCSV, postJSON} from "../../utils/api";
import CommonTableSingle from "../../components/CommonTableSingle";

export default {
  components: {CommonTableSingle},
  name: "Particle",
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
      particle: {
        sampleProperty: "",
        sampleList: [],
        sampleLabel: [],
        sampleId: "",   // 选中的样品id
        selectRow: ""
      },
      options: [
        {value: '源样品', label: this.$t('Sample.PostSourceSample.sampleProperty')},
        {value: '配置样品', label: this.$t('Sample.PostConfigSample.sampleProperty')},
        {value: '样品', label: this.$t('Sample.PostActualSample.sampleProperty')},
      ],
      tableLabel: {
        solid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        solid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        liquid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
        liquid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
      }
    }
  },
  mounted() {
    this.$bus.$on('returnSampleIdSingle', (data) => {
      if (data.function === 'particle') {
        this.particle.sampleId = data.sample.id;
        this.particle.selectRow = data.sample;
      }
    })
  },
  async activated() {
    await postJSON('/batch/getBatchListStandard').then((resp) => {
      this.batchListStandard = resp.data.result.batchList
    })
  },
  watch: {
    'particle.selectRow': {
      handler() {
        this.btnShow = 'none'
      }
    },
    'batchInfo.batchId': {
      handler() {
        // 清空所有用户输入内容
        this.particle = {
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
    'particle.sampleProperty': {
      handler() {
        this.particle.sampleId = ""
        this.particle.selectRow = ""
        this.urls = ""
        if (this.particle.sampleProperty === "源样品") {
          this.particle.sampleList = this.batchInfo.sampleList.sourceSampleList;
          this.particle.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_normal : this.tableLabel.liquid_normal
        } else if (this.particle.sampleProperty === "配置样品") {
          this.particle.sampleList = this.batchInfo.sampleList.configSampleList;
          this.particle.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_config : this.tableLabel.liquid_config
        } else if (this.particle.sampleProperty === "样品") {
          this.particle.sampleList = this.batchInfo.sampleList.actualSampleList;
          this.particle.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_normal : this.tableLabel.liquid_normal
        } else {
          this.particle.sampleList = []
          this.particle.sampleLabel = []
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
    runParticle() {
      if (this.particle.sampleId === "" || this.particle.sampleProperty === "") {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/analysis/particle', {
        sampleId: this.particle.sampleId,
        sampleProperty: this.particle.sampleProperty,
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
    // 单颗粒计数
    downloadFile(fileName) {
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      let name = ''
      if (fileName === 'particleCounts')
        name = this.$t('Analysis.Particle.btn.particleCounts')
      else if (fileName === 'particleConc')
        name = this.$t('Analysis.Particle.btn.particleConc')
      else if (fileName === 'dissolvedConc')
        name = this.$t('Analysis.Particle.btn.dissolvedConc')
      else if (fileName === 'massRatio')
        name = this.$t('Analysis.Particle.btn.massRatio')
      else if (fileName === 'particleMass')
        name = this.$t('Analysis.Particle.btn.particleMass')
      else if (fileName === 'particleSize')
        name = this.$t('Analysis.Particle.btn.particleSize')
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