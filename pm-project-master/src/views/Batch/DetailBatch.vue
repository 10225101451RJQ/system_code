<template>
  <div>
    <h3>{{ $t('Batch.DetailBatch.title') }}</h3>
    <el-descriptions :column="5" border title="">
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.batchName') }}</b></template>
        {{ batchInfo.batchName }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.authorName') }}</b></template>
        {{ batchInfo.authorName }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.position') }}</b></template>
        {{ batchInfo.position }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.analysisType') }}</b></template>
        {{ batchInfo.analysisType }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.sampleState') }}</b></template>
        {{ batchInfo.sampleState }}
      </el-descriptions-item>
      <!--      实验参数-->
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.TE') }}</b></template>
        {{ batchInfo.parameters.TE }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.Cp') }}</b></template>
        {{ batchInfo.parameters.Cp + ' ' + $t('Batch.DetailBatch.batchInfo.particles_mL') }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.V') }}</b></template>
        {{ batchInfo.parameters.V }} mL/min
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.T ') }}</b></template>
        {{ batchInfo.parameters.T }} s
      </el-descriptions-item>
      <el-descriptions-item>
        <template slot="label"><b>{{ $t('Batch.DetailBatch.batchInfo.Vi') }}</b></template>
        {{ batchInfo.parameters.Vi }} mL
      </el-descriptions-item>
    </el-descriptions>
    <div class="title">
      <h4>{{ $t('Sample.PostStandardSample.sampleProperty') }}</h4>
      <el-tag class="title-tag" type="primary">{{ $t('Sample.PostStandardSample.introduction') }}</el-tag>
      <el-button class="sampleButton" icon="el-icon-upload" plain size="medium" type="primary"
                 @click="postSample('postStandardSample')">{{ $t('Sample.PostStandardSample.title') }}
      </el-button>
    </div>
    <common-table :table-data="sampleList.standardSampleList"
                  :table-label="tableLabel.standardSample"></common-table>
    <div class="title">
      <h4>{{ $t('Sample.PostSourceSample.sampleProperty') }}</h4>
      <el-tag class="title-tag" type="success">{{ $t('Sample.PostSourceSample.introduction') }}</el-tag>
      <el-button class="sampleButton" icon="el-icon-upload" plain size="medium" type="primary"
                 @click="postSample('postSourceSample')">{{ $t('Sample.PostSourceSample.title') }}
      </el-button>
    </div>
    <common-table :table-data="sampleList.sourceSampleList"
                  :table-label="batchInfo.sampleState==='固体' || batchInfo.sampleState==='solid'?tableLabel.solid_normal:tableLabel.liquid_normal"></common-table>
    <div class="title">
      <h4>{{ $t('Sample.PostConfigSample.sampleProperty') }}</h4>
      <el-tag class="title-tag" type="warning">{{ $t('Sample.PostConfigSample.introduction') }}</el-tag>
      <el-button class="sampleButton" icon="el-icon-upload" plain size="medium" type="primary"
                 @click="postSample('postConfigSample')">{{ $t('Sample.PostConfigSample.title') }}
      </el-button>
    </div>
    <common-table :table-data="sampleList.configSampleList"
                  :table-label="batchInfo.sampleState==='固体' || batchInfo.sampleState==='solid'?tableLabel.solid_config:tableLabel.liquid_config"></common-table>
    <div class="title">
      <h4>{{ $t('Sample.PostActualSample.sampleProperty') }}</h4>
      <el-button class="sampleButton" icon="el-icon-upload" plain size="medium" type="primary"
                 @click="postSample('postActualSample')">{{ $t('Sample.PostActualSample.title') }}
      </el-button>
    </div>
    <common-table-operation
        :table-data="sampleList.actualSampleList"
        :table-label="batchInfo.sampleState==='固体' || batchInfo.sampleState==='solid'?tableLabel.solid_normal:tableLabel.liquid_normal"
        blue-btn-show="none"
        @del='delSample'></common-table-operation>
    <div class="title">
      <h4>{{ $t('Sample.PostBlankSample.sampleProperty') }}</h4>
      <el-button class="sampleButton" icon="el-icon-upload" plain size="medium" type="primary"
                 @click="postSample('postBlankSample')">{{ $t('Sample.PostBlankSample.title') }}
      </el-button>
    </div>
    <common-table-operation
        :table-data="sampleList.blankSampleList"
        :table-label="batchInfo.sampleState==='固体' || batchInfo.sampleState==='solid'?tableLabel.solid_blank:tableLabel.liquid_blank"
        blue-btn-show="none"
        @del='delSample'></common-table-operation>
  </div>
</template>

<script>
import CommonTable from "../../components/CommonTable";
import CommonTableOperation from "../../components/CommonTableOperation";
import {postFormData, postJSON} from "../../utils/api";
import Cookie from "js-cookie";

export default {
  components: {CommonTableOperation, CommonTable},
  name: 'DetailBatch',
  data() {
    return {
      // 总信息
      batchInfo: {
        id: this.$route.query.id,
        batchName: "",
        authorName: "",
        position: "",
        sampleState: "",
        analysisType: "",
        parameters: {Cp: "", V: "", T: "", Vi: "", TE: ""},
      },
      // 列表表头
      tableLabel: {
        // 固体
        standardSample: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
        ],
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
        solid_blank: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Vf", label: this.$t('Batch.DetailBatch.tableOperation.options.Vf')},
          {prop: "m", label: this.$t('Batch.DetailBatch.tableOperation.options.m')},
        ],
        // 液体
        liquid_normal: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
        liquid_config: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "sourceMass", label: this.$t('Batch.DetailBatch.tableOperation.options.sourceMass')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
        liquid_blank: [
          {prop: "sampleName", label: this.$t('Batch.DetailBatch.tableOperation.options.sampleName')},
          {prop: "Df", label: this.$t('Batch.DetailBatch.tableOperation.options.Df')},
        ],
      },
      // 4种样品列表
      xSampleList: "",
      sampleList: {
        sourceSampleList: [],
        standardSampleList: [],
        configSampleList: [],
        actualSampleList: [],
        blankSampleList: [],
      }
    };
  },
  created() {
    this.getBatchInfo();
  },
  mounted() {
  },
  methods: {
    // 获取某一批次信息
    getBatchInfo() {
      postJSON('/batch/getBatchInfo', {batchId: this.$route.query.id}).then((resp) => {
        this.batchInfo = resp.data.result.batchInfo;
        if (Cookie.get('language') === 'en') {
          if (this.batchInfo.sampleState === '固体')
            this.batchInfo.sampleState = 'solid'
          else this.batchInfo.sampleState = 'liquid'
          if (this.batchInfo.analysisType === '迭代法')
            this.batchInfo.analysisType = 'iteration'
          else this.batchInfo.analysisType = 'poisson'
        }
        this.sampleList = resp.data.result.sampleList;
      });
    },
    /* 普通页面函数 */
    back() {
      this.$router.back()
    },
    edit() {
      // this.$router.push({name: "postBatch", query: {batchInfo: this.batchInfo}})
    },
    // 上传新的样品
    postSample(type) {
      this.$router.push({
        name: 'batch_' + type,
        query: {
          batchId: this.batchInfo.id,
          batchName: this.batchInfo.batchName,
          sampleState: this.batchInfo.sampleState,
        }
      });
    },
    delSample(row) {
      this.$confirm(this.$t('Common.confirm.msg.delete'), this.$t('Common.confirm.title'), {
        confirmButtonText: this.$t('Common.confirm.btn.ok'),
        cancelButtonText: this.$t('Common.confirm.btn.cancel'),
        type: 'warning'
      }).then(() => {
        console.log(row.id)
        postFormData('/delete/deleteOneSample', {id: row.id}).then((resp) => {
          if (resp.data.code === 0) {
            this.$message({type: 'success', message: resp.data.message});
            this.getBatchInfo()
          } else this.$message({type: 'warning', message: resp.data.message});
        })
      }).catch(() => {
        this.$message({type: 'info', message: this.$t('Common.message.cancelText')});
      });
    }
  }
}

</script>

<style lang="less" scoped>
h3 {
  margin-top: 0;
}

h4 {
  align-self: center;
}

.title {
  display: flex;
  justify-content: flex-start;
}

.title-tag {
  align-self: center;
  margin-left: 10px;
}

.sampleButton {
  margin-left: auto;
  align-self: center
}

.el-button {
  color: #3ab5b0;
}

.el-button--primary.is-active,
.el-button--primary:active {
  background: #3ab5b0;
  border-color: #3ab5b0;
  color: #fff;
}

.el-button--primary:focus,
.el-button--primary:hover {
  background: #3ab5b0;
  border-color: #3ab5b0;
  color: #fff;
}

/deep/ .el-collapse-item__header {
  font-size: 18px;
  font-weight: bolder;
  color: #1B63AD;
}

</style>