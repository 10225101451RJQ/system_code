<template>
  <!-- 源样品指纹分析 -->
  <div>
    <!-- 批次选择模块 -->
    <div>
      <el-row>
        <el-col :span=3>
          <el-button plain style="width: 95%" type="success">
            <b>{{ $t('Analysis.common.select.batch.label') }}</b></el-button>
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
      <h4>{{ $t('Analysis.AnalysisSource.createGroup.title') }}</h4>
      <el-form ref="groupForm" :inline="true" :model="source_fp" label-width="120px" style="margin-top: 10px">
        <!--      <div v-for="(item,index) in source_fp.dynamicItem" :key="index" style="display: flex">-->
        <!--        <el-form-item :label="item.sourceName"-->
        <!--                      :prop="'dynamicItem.'+index+'.sourceX'"-->
        <!--                      :rules="{required:true, validator:vali, trigger:'blur'}">-->
        <!--          <el-input v-model="item.sourceX" placeholder="请输入x"></el-input>-->
        <!--        </el-form-item>-->
        <!--      </div>-->
        <div v-for="(item,index) in source_fp.dynamicItem" :key="index" style="display: flex">
          <el-form-item :label="item.sourceName"
                        :prop="'dynamicItem.'+index+'.sourceX'"
                        :rules="{required:true, validator:vali, trigger:'blur'}">
            <el-select v-model="item.sourceX" :placeholder="$t('Analysis.AnalysisSource.createGroup.support.rule')"
                       clearable>
              <el-option v-for="item in item.options" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </div>
        <div>
          <el-form-item :label="$t('Analysis.AnalysisSource.createGroup.logBase.label')" label-width="120px"
                        :rules="{required:true, validator:vali, trigger:'blur'}"
                        prop="input_logBase">
            <el-input v-model="source_fp.input_logBase"
                      :placeholder="$t('Analysis.AnalysisSource.createGroup.logBase.rule')"
                      class="input-box"></el-input>
          </el-form-item>
        </div>
        <div>
          <el-form-item :label="$t('Batch.PostBatch.configurationSamplesMass.title')" label-width="120px" prop="file">
            <el-upload
                ref="upload1"
                :auto-upload="false"
                :before-upload="handleBeforeUpload"
                :file-list="fileList1"
                :http-request="httpRequest"
                :limit="2"
                :multiple="false"
                :on-change="handleChange1"
                :on-exceed="handleExceed1"
                :on-preview="handlePreview"
                :on-remove="handleRemove1"
                accept="text/csv"
                action=""
                class="upload-demo">
              <el-button slot="trigger" plain size="small" type="primary">
                {{ $t('Sample.common.sampleFile.selectBtn') }}
              </el-button>
              <div slot="tip" class="el-upload__tip">configuration_samples_mass.csv</div>
            </el-upload>
          </el-form-item>
        </div>
        <div>
          <el-form-item>
            <el-button type="primary" @click="generateSourceGroup">
              {{ $t('Analysis.AnalysisSource.createGroup.logBase.btn') }}
            </el-button>
          </el-form-item>
        </div>
      </el-form>
      <!-- 分组列表展示 -->
      <h4>{{ $t('Analysis.AnalysisSource.analysis.title') }}</h4>
      <common-table-single :table-data="source_fp.groupList"
                           :table-label="tableLabel.group"
                           function="source"></common-table-single>
      <h5>{{ show.groupString }}</h5>
      <el-descriptions :column="4" :title="$t('Analysis.AnalysisSource.analysis.subTitle')" border
                       style="margin-bottom: 10px">
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.AnalysisSource.analysis.functions.fp') }}</template>
          <el-button plain size="mini" type="primary" @click="downloadFp">
            {{ $t('Analysis.common.btn.download') }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.AnalysisSource.analysis.functions.train') }}</template>
          <el-button plain size="mini" type="primary" @click="downloadTrain">
            {{ $t('Analysis.common.btn.download') }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.AnalysisSource.analysis.functions.sourceParticleConc') }}</template>
          <el-button plain size="mini" type="primary" @click="downloadSourceParticleConc">
            {{ $t('Analysis.common.btn.show') }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">{{
              $t('Analysis.AnalysisSource.analysis.functions.sourceParticleContribution')
            }}
          </template>
          <el-button plain size="mini" type="primary" @click="downloadSourceParticleContribution">
            {{ $t('Analysis.common.btn.download') }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.AnalysisSource.analysis.functions.model.label') }}</template>
          <el-select v-model="source_fp.modelType"
                     :placeholder="$t('Analysis.AnalysisSource.analysis.functions.model.rule')" clearable
                     size="mini" style="width: 150px">
            <el-option v-for="item in modelTypeOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <el-button plain size="mini" style="margin-left: 10px" type="primary" @click="generateModel">
            {{ $t('Analysis.common.btn.generate') }}
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">{{ $t('Analysis.common.chart.heatMap') }}</template>
          <el-select v-model="source_fp.heatMapType" :placeholder="$t('Analysis.common.select.sampleProperty.rule')"
                     clearable size="mini">
            <el-option v-for="item in samplePropertyOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <el-button plain size="mini" style="margin-left: 10px" type="primary" @click="generateHeatMap()">
            {{ $t('Analysis.common.btn.generate') }}
          </el-button>
          <el-button plain size="mini" style="margin-left: 5px" type="primary" @click="downloadHeatMapData('source')">
            {{ $t('Analysis.common.btn.downloadHeatMapData') }}
          </el-button>
        </el-descriptions-item>
      </el-descriptions>
      <!--绘图区-->
      <el-tabs v-model="tabActiveName" style="margin-top: 10px" type="border-card">
        <el-tab-pane :label="$t('Analysis.common.chart.heatMap')" name="HeatMap">
          <HeatMapSource :heat-map-info="heatMapInfo" heat-map-id="heatMapSource"></HeatMapSource>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import CommonTableSingle from "../../components/CommonTableSingle";
import HeatMapSource from "../Chart/HeatMap";
import {downloadCSV, postFormData, postJSON} from "../../utils/api";

export default {
  name: "AnalysisSource",
  components: {CommonTableSingle, HeatMapSource},
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
    let valiNumPositivePass = (rule, value, callback) => {
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
      fileList1: [],
      contentShow: "none",
      batchListStandard: [],
      batchInfo: {
        batchId: "",
      },
      heatMapInfo: "",
      tabActiveName: "HeatMap",
      source_fp: {
        modelType: "",
        dynamicItem: [],
        input_logBase: "",
        groupList: [],
        groupId: "",    // 选中的组id
        heatMapType: "",
        selectRow: ""
      },
      rules: {
        input_logBase: [{
          required: true,
          message: this.$t('Analysis.AnalysisSource.createGroup.logBase.rule'),
          trigger: "blur"
        }],
      },
      vali: valiNumDotPass,
      tableLabel: {
        group: [
          {prop: "source", label: this.$t('Analysis.AnalysisSource.analysis.table.options.source')},
          {prop: "logBase", label: this.$t('Analysis.AnalysisSource.analysis.table.options.logBase')},
          {prop: "isModel", label: this.$t('Analysis.AnalysisSource.analysis.table.options.isModel')},
        ]
      },
      samplePropertyOptions: [],
      modelTypeOptions: [
        {label: "RF", value: "RFModel"},
        {label: "XGB", value: "XGBoostModel"},
        {label: "SVM", value: "SVMModel"},
        {label: "GaussianNB", value: "GaussianNBModel"}],
      show: {
        groupString: ""
      }
    }
  },
  mounted() {
    this.$bus.$on('returnSampleIdSingle', (data) => {
      if (data.function === 'source') {
        this.source_fp.groupId = data.sample.id;
        this.source_fp.selectRow = data.sample;
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
        // 清空所有用户输入内容
        this.fileList1 = ""
        this.source_fp = {
          modelType: "",
          dynamicItem: [],
          input_logBase: "",
          groupList: [],
          groupId: "",    // 选中的组id
          heatMapType: "",
          selectRow: ""
        }
        this.show.groupString = ""
        // batchId为空时清空所有用户输入内容
        if (this.batchInfo.batchId === "") {
          this.contentShow = "none"
        } else {
          this.contentShow = ""
          // batchId变化且不为空时重新获取对应id的内容
          // 这里的getBatchInfo可改成getGroupList
          this.getBatchInfo()
        }
      }
    },
    'source_fp.selectRow': {
      handler() {
        if (this.source_fp.selectRow === "")
          this.show.groupString = ""
        else this.show.groupString = this.$t('Analysis.AnalysisSource.analysis.group.showString.str_1') + this.source_fp.selectRow.source +
            this.$t('Analysis.AnalysisSource.analysis.group.showString.str_2') + this.source_fp.selectRow.logBase;
      }
    }
  },
  methods: {
    // 文件上传
    httpRequest(param) { // submitUpload重复调用httpRequest，达到效果
    },
    handleBeforeUpload(file) {
      if (this.fileList1.length !== 1)
        this.$message.error(this.$t('Sample.common.sampleFile.rule.exceedFile_1'));
    },
    handleSuccess(res, file) {
    },
    handleChange1(file, fileList) {
      if (this.$refs.upload1.uploadFiles.length > 1)
        this.$refs.upload1.uploadFiles.shift()
      if (this.$refs.upload1.uploadFiles.length > 0)
        this.fileList1 = this.$refs.upload1.uploadFiles
    },
    // handleChange2(file, fileList) {
    //   if (this.$refs.upload2.uploadFiles.length > 1)
    //     this.$refs.upload2.uploadFiles.shift()
    //   if (this.$refs.upload2.uploadFiles.length > 0)
    //     this.fileList2 = this.$refs.upload2.uploadFiles
    // },
    handleRemove1(file, fileList) {
      this.fileList1 = fileList;
    },
    // handleRemove2(file, fileList) {
    //   this.fileList2 = fileList;
    // },
    handlePreview(file) {
    },
    handleExceed1() {
      this.$message.error(this.$t('Sample.common.sampleFile.rule.exceedFile_1'));
    },
    // handleExceed2() {
    //   this.$message.error(this.$t('Sample.common.sampleFile.rule.exceedFile_1'));
    // },
    // 生成纯物质分组
    async generateSourceGroup() {
      if (this.batchInfo.batchId === "" || this.source_fp.dynamicItem.length === 0) {
        this.$message.error(this.$t('Analysis.common.select.msg.emptySelect'))
        return
      }
      if (this.fileList1.length !== 1) {
        this.$message.error(this.$t('Sample.common.sampleFile.rule.empty'))
        return
      }
      await this.$refs.groupForm.validate((valid) => {
        if (valid) {
          let uploadData = new FormData(); // 用FormData存放上传文件
          this.fileList1.forEach(file => {
            uploadData.append('configuration_samples_mass', file.raw)
          })
          uploadData.append('batchId', this.batchInfo.batchId)
          uploadData.append('sourceList', JSON.stringify(this.source_fp.dynamicItem))
          uploadData.append('logBase', this.source_fp.input_logBase)

          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });

          postFormData('/analysis/generateSourceGroup', uploadData).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
                confirmButtonText: this.$t('Common.confirm.btn.ok'),
                type: 'success'
              })
              this.getSourceGroupList()
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
          })
        } else {
          return false
        }
      })
    },
    // 获取某一批次信息
    async getBatchInfo() {
      if (this.batchInfo.batchId === "")
        this.$message.error(this.$t('Analysis.common.select.batch.rule'))
      await postJSON('/batch/getAllSourceSampleX', {batchId: this.batchInfo.batchId}).then((resp) => {
        if (resp.data.code === 0) {
          this.source_fp.dynamicItem = []
          this.samplePropertyOptions = []
          for (let i = 0; i < resp.data.result.sourceList.length; i++) {
            this.source_fp.dynamicItem.push({
              sourceName: resp.data.result.sourceList[i].sourceName,
              sourceX: "",
              options: resp.data.result.sourceList[i].supportXValues,
            })
            this.samplePropertyOptions.push({
              value: resp.data.result.sourceList[i].sourceName,
              label: resp.data.result.sourceList[i].sourceName,
            })
          }
          this.getSourceGroupList();
          this.$message.success(resp.data.message)
        } else {
          this.$message.warning(resp.data.message)
        }
      });
    },
    // 获取纯物质分组列表
    getSourceGroupList() {
      postJSON('/batch/getSourceGroupList', {
        batchId: this.batchInfo.batchId
      }).then((resp) => {
        this.source_fp.groupList = resp.data.result.groupList;
      });
    },
    // 下载n种物质的fp文件
    downloadFp() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      // 源样品颗粒数浓度(列表)
      for (let i = 0; i < this.source_fp.dynamicItem.length; i++) {
        const loading = this.$loading({
          lock: true,
          text: this.$t('Common.loading.text'),
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        postJSON('/fileExist/fpCSV', {
          groupId: this.source_fp.groupId,
          sampleType: this.samplePropertyOptions[i].value
        }).then((resp) => {
          loading.close();
          if (resp.data.code === 0) {
            this.$message.success(resp.data.message)
            postJSON('/download/fpCSV', {
              groupId: this.source_fp.groupId,
              sampleType: this.samplePropertyOptions[i].value
            }).then((resp) => {
              downloadCSV(resp, this.$t('Analysis.AnalysisSource.analysis.functions.fp') + "-" +
                  this.samplePropertyOptions[i].value + "_" +
                  this.batchInfo.batchId + "_" +
                  this.source_fp.selectRow.source + "_" +
                  this.source_fp.selectRow.logBase)
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
      }
    },
    // 下载源样品颗粒数浓度
    downloadSourceParticleConc() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/download/sourceParticleConcCSV', {
        groupId: this.source_fp.groupId,
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$alert(resp.data.result.string,
              this.$t('Analysis.AnalysisSource.analysis.functions.sourceParticleConc'),
              {confirmButtonText: this.$t('Common.confirm.btn.ok'),});
        } else if (resp.data.code === 1)
          this.$message.error(resp.data.message)
      });
    },
    // 下载纯物质某分组的train.csv
    downloadTrain() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/fileExist/trainCSV', {
        groupId: this.source_fp.groupId,
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$message.success(resp.data.message)
          postJSON('/download/trainCSV', {
            groupId: this.source_fp.groupId,
          }).then((resp) => {
            downloadCSV(resp, this.$t('Analysis.AnalysisSource.analysis.functions.train') + "-" +
                this.batchInfo.batchId + "_" +
                this.source_fp.selectRow.source + "_" +
                this.source_fp.selectRow.logBase)
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
    },
    // 下载各源样品颗粒数贡献
    downloadSourceParticleContribution() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/fileExist/sourceParticleContributionCSV', {
        groupId: this.source_fp.groupId,
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$message.success(resp.data.message)
          postJSON('/download/sourceParticleContributionCSV', {
            groupId: this.source_fp.groupId,
          }).then((resp) => {
            loading.close();
            downloadCSV(resp, this.$t('Analysis.AnalysisSource.analysis.functions.sourceParticleContribution') + "-" +
                this.batchInfo.batchId + "_" +
                this.source_fp.selectRow.source + "_" +
                this.source_fp.selectRow.logBase)
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
    },
    // 生成热力图
    generateHeatMap() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      if (this.source_fp.heatMapType === "") {
        this.$message.error(this.$t('Sample.common.sampleType.rule'))
        return
      }
      this.heatMapInfo = {
        type: 'source',
        groupId: this.source_fp.groupId,
        fileId: "",
        heatMapType: this.source_fp.heatMapType,
        logBase: "",
      }
    },
    // 下载热力图数据文件
    downloadHeatMapData() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      if (this.source_fp.heatMapType === "") {
        this.$message.error(this.$t('Sample.common.sampleType.rule'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/fileExist/heatMapDataCSV', {
        id: this.source_fp.groupId,
        sampleProperty: "source",
        sampleType: this.source_fp.heatMapType,
        logBase: "",
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$message.success(resp.data.message)
          postJSON('/download/heatMapDataCSV', {
            id: this.source_fp.groupId,
            sampleProperty: "source",
            sampleType: this.source_fp.heatMapType,
            logBase: "",
          }).then((resp) => {
            loading.close();
            downloadCSV(resp, this.$t("Analysis.common.chart.heatMap") + "-" +
                this.$t("Sample.PostSourceSample.sampleProperty") + "-" +
                this.batchInfo.batchId + "_" +
                this.source_fp.selectRow.source + "_" +
                this.source_fp.selectRow.logBase)
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

    },
    // 生成模型
    generateModel() {
      if (this.source_fp.groupId === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.group.rule'))
        return
      }
      if (this.source_fp.modelType === "") {
        this.$message.error(this.$t('Analysis.AnalysisSource.analysis.functions.model.rule'))
        return
      }
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postJSON('/analysis/model', {
        groupId: this.source_fp.groupId,
        modelType: this.source_fp.modelType
      }).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$confirm(resp.data.message, this.$t('Common.confirm.title'), {
            confirmButtonText: this.$t('Common.confirm.btn.ok'),
            type: 'success'
          }).then(() => {
          })
          this.getSourceGroupList();
          this.show.groupString = ""
          this.$bus.$emit("updateModelList")
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
.div {
  margin-top: 10px;
}
</style>