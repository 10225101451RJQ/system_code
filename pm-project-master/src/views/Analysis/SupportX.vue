<template>
  <!-- 指纹提取 -->
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
    <div :style="{'margin-top':'10px','margin-bottom':'10px'}">
      <el-row>
        <el-col :span=3>
          <el-button plain style="width: 95%" type="success">
            <b>{{ $t('Analysis.common.select.sampleProperty.label') }}</b></el-button>
        </el-col>
        <el-col :span=6>
          <el-select v-model="supportX.sampleProperty" :placeholder="$t('Analysis.common.select.sampleProperty.rule')"
                     clearable>
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <common-table-multiple v-if="isReloadData"
                             :table-data="supportX.sampleList"
                             :table-label="supportX.sampleLabel"
                             function="supportX"></common-table-multiple>
      <el-form ref="logBaseForm" :inline="true" :model="supportX" :rules="rules" label-width="80px">
        <el-form-item :label="$t('Analysis.SupportX.support.label')" prop="x">
          <el-input v-model="supportX.x" :placeholder="$t('Analysis.SupportX.support.rule_1')"
                    style="width: 200px"></el-input>
        </el-form-item>
        <el-button type="primary" @click="runSupportX()">{{ $t('Analysis.common.btn.runAnalysis') }}</el-button>
      </el-form>
    </div>
  </div>
</template>

<script>
import {postJSON} from "../../utils/api";
import CommonTableMultiple from "../../components/CommonTableMultiple";

export default {
  name: "SupportX",
  components: {CommonTableMultiple},
  data() {
    //包含小数的数字
    let valiNumDotPass = (rule, value, callback) => {
      let reg = /^[+-]?(0|([1-9]\d*))(\.\d+)?$/g;
      if (value === '') {
        callback(new Error(this.$t('Common.numRule.empty')));
      } else if (!reg.test(value)) {
        callback(new Error(this.$t('Common.numRule.num')));
      } else {
        if (this.supportX.sampleProperty === "源样品") {
          if (value < 0.001 || value > 0.009) {
            callback(new Error(this.$t('Analysis.SupportX.support.rule_2')))
          } else {
            callback();
          }
        } else if (this.supportX.sampleProperty !== "") {
          // 对于!==0.1，关于为啥不能直接判断，我也不知道，哈哈
          // 所以要写成 < 0.1 || > 0.1
          if (value <= 0 || value >= 1) {
            callback(new Error(this.$t('Analysis.SupportX.support.rule_3')))
          } else {
            callback();
          }
        }
      }
    };
    return {
      isReloadData: true,
      contentShow: "none",
      batchListStandard: [],
      batchInfo: {
        batchId: "",
        sampleState: "",
        sampleList: {},
      },
      supportX: {
        x: "",
        sampleProperty: "",
        sampleList: [],   // 某个type的list
        sampleLabel: [],  // 某个type的label
        sampleId: [],     // 选中的样品id
        selectRow: []
      },
      rules: {
        x: [{required: true, validator: valiNumDotPass, trigger: "blur"}]
      },
      placeHolder: "",
      options: [
        {value: '源样品', label: this.$t('Sample.PostSourceSample.sampleProperty')},
        {value: '配置样品', label: this.$t('Sample.PostConfigSample.sampleProperty')},
        {value: '样品', label: this.$t('Sample.PostActualSample.sampleProperty')},
      ],
      tableLabel: {
        solid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "supportXList", label: this.$t('Batch.DetailBatch.tableOperation.options.supportXList')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        solid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "supportXList", label: this.$t('Batch.DetailBatch.tableOperation.options.supportXList')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        liquid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "supportXList", label: this.$t('Batch.DetailBatch.tableOperation.options.supportXList')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
        liquid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "supportXList", label: this.$t('Batch.DetailBatch.tableOperation.options.supportXList')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
      }
    }
  },
  mounted() {
    this.$bus.$on('returnSampleIdMultiple', (data) => {
      if (data.function === 'supportX') {
        this.supportX.sampleId = []
        for (let i in data.samples)
          this.supportX.sampleId.push(data.samples[i].id)
        this.supportX.selectRow = data.samples;
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
        this.supportX = {
          x: "",
          sampleProperty: "",
          sampleList: [],   // 某个type的list
          sampleLabel: [],  // 某个type的label
          sampleId: [],     // 选中的样品id
          selectRow: []
        }
        this.batchInfo.sampleList = []
        this.batchInfo.sampleState = ""
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
    'supportX.sampleProperty': {
      handler() {
        this.supportX.sampleId = []
        this.supportX.selectRow = []
        if (this.supportX.sampleProperty === "源样品") {
          this.supportX.sampleList = this.batchInfo.sampleList.sourceSampleList;
          this.supportX.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_normal : this.tableLabel.liquid_normal
        } else if (this.supportX.sampleProperty === "样品") {
          this.supportX.sampleList = this.batchInfo.sampleList.actualSampleList;
          this.supportX.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_normal : this.tableLabel.liquid_normal
        } else if (this.supportX.sampleProperty === "配置样品") {
          this.supportX.sampleList = this.batchInfo.sampleList.configSampleList;
          this.supportX.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_config : this.tableLabel.liquid_config
        } else {
          this.supportX.sampleList = []
          this.supportX.sampleLabel = []
        }
      }
    },
    "batchInfo.sampleList": {
      // 当重新获取batchInfo时，局部更新掉列表中的内容
      handler() {
        if (this.supportX.sampleProperty === "源样品") {
          this.supportX.sampleList = this.batchInfo.sampleList.sourceSampleList;
          this.supportX.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_normal : this.tableLabel.liquid_normal
        } else if (this.supportX.sampleProperty === "样品") {
          this.supportX.sampleList = this.batchInfo.sampleList.actualSampleList;
          this.supportX.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_normal : this.tableLabel.liquid_normal
        } else if (this.supportX.sampleProperty === "配置样品") {
          this.supportX.sampleList = this.batchInfo.sampleList.configSampleList;
          this.supportX.sampleLabel = this.batchInfo.sampleState === "固体" ? this.tableLabel.solid_config : this.tableLabel.liquid_config
        }
      }
    },
  },
  methods: {
    // 局部刷新当前页面
    reloadPart() {
      this.isReloadData = false;
      this.$nextTick(() => {
        this.isReloadData = true
      })
    },
    // 获取某一批次信息
    getBatchInfo() {
      if (this.batchInfo.batchId === "") {
        this.$message.error(this.$t('Analysis.common.select.batch.rule'))
        return
      }
      postJSON('/batch/getBatchInfo', {batchId: this.batchInfo.batchId}).then((resp) => {
        if (resp.data.code === 0) {
          this.batchInfo.sampleState = resp.data.result.batchInfo.sampleState
          this.batchInfo.sampleList = resp.data.result.sampleList;
          this.$message.success(resp.data.message)
        } else {
          this.$message.warning(resp.data.message)
        }
      });
    },
    runSupportX() {
      if (this.supportX.sampleId.length === 0 || this.supportX.sampleProperty === "") {
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
          postJSON('/analysis/generateSupportXFile', {
            sampleId: this.supportX.sampleId.toString(),
            sampleProperty: this.supportX.sampleProperty,
            support: this.supportX.x,
          }).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              // 全局事件总线，更新内容
              this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
                confirmButtonText: this.$t('Common.confirm.btn.ok'),
                type: 'success'
              }).then(() => {
                // this.batchInfo.batchId=""
                this.getBatchInfo();   // 如果更新不好使则将id置空
                this.supportX.sampleId = []
              }).catch(() => {
                this.getBatchInfo();   // 如果更新不好使则将id置空
                this.supportX.sampleId = []
              })
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
        } else return false
      })
    },
  },
}
</script>

<style lang="less" scoped>
</style>