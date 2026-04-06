<template>
  <div>
    <el-form ref="batchForm" :model="batchInfo" :rules="rules">
      <h4>{{ $t('Batch.PostBatch.basicInfo.title') }}</h4>
      <el-row>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.basicInfo.batchName.label')" label-width="100px" prop="batchName">
            <el-input v-model="batchInfo.batchName"
                      :placeholder="$t('Batch.PostBatch.basicInfo.batchName.rule')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.basicInfo.position.label')" label-width="100px" prop="position">
            <el-input v-model="batchInfo.position"
                      :placeholder="$t('Batch.PostBatch.basicInfo.position.rule')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.basicInfo.sampleState.label')"
                        label-width="100px" prop="sampleState">
            <el-select v-model="batchInfo.sampleState" :placeholder="$t('Batch.PostBatch.basicInfo.sampleState.rule')"
                       clearable>
              <el-option v-for="item in sampleStateOptions" :key="item.value" :label="item.label"
                         :value="item.value"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.basicInfo.analysisType.label')" label-width="100px"
                        prop="analysisType">
            <el-select v-model="batchInfo.analysisType"
                       :placeholder="$t('Batch.PostBatch.basicInfo.analysisType.rule')"
                       clearable>
              <el-option v-for="item in analysisTypeOptions" :key="item.value" :label="item.label"
                         :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <h4>{{ $t('Batch.PostBatch.params.title') }}</h4>
      <el-row>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.params.Cp.label')" label-width="130px" prop="Cp">
            <el-input v-model="Cp" :placeholder="$t('Batch.PostBatch.params.Cp.rule')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.params.CpBase.label')" label-width="130px" prop="CpBase">
            <el-input v-model="batchInfo.CpBase" :placeholder="$t('Batch.PostBatch.params.CpBase.rule')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.params.CpExponent.label')" label-width="130px" prop="CpExponent">
            <el-input v-model="batchInfo.CpExponent"
                      :placeholder="$t('Batch.PostBatch.params.CpExponent.rule')"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.params.Vi.label')" label-width="130px" prop="Vi">
            <el-input v-model="Vi" :placeholder="$t('Batch.PostBatch.params.Vi.rule')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.params.V.label')" label-width="130px" prop="V">
            <el-input v-model="batchInfo.V" :placeholder="$t('Batch.PostBatch.params.V.rule')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Batch.PostBatch.params.T.label')" label-width="130px" prop="T">
            <el-input v-model="batchInfo.T" :placeholder="$t('Batch.PostBatch.params.T.rule')"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <h4>{{ $t('Batch.PostBatch.sampleType.title') }}</h4>
      <el-row>
        <el-col :span=24>
          <div v-for="(item,index) in batchInfo.dynamicItem" :key="index" style="display: flex">
            <el-form-item :prop="'dynamicItem.'+index+'.sourceName'"
                          :rules="{ required:true, message:$t('Batch.PostBatch.sampleType.rule'), trigger:'blur'}"
                          label=" " label-width="30px">
              <el-input v-model="item.sourceName" size="medium"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button v-if="index+1===batchInfo.dynamicItem.length"
                         plain size="medium" style="margin-left: 5px" type="primary"
                         @click="addItem">{{ $t('Batch.PostBatch.sampleType.addBtn') }}
              </el-button>
              <el-button v-if="index!==0" plain size="medium" style="margin-left: 5px" type="danger"
                         @click="deleteItem(item,index)">
                {{ $t('Batch.PostBatch.sampleType.delBtn') }}
              </el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <h4 style="margin-bottom: 0">{{ $t('Batch.PostBatch.uploadFile') }}</h4>
      <el-row>
        <el-col :span=12>
          <h5>{{ $t('Batch.PostBatch.calibrationCurvesFile.title') }}</h5>
          <el-form-item label="calibration_curves.csv" label-width="170px" prop="file">
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
              <!-- <div slot="tip" class="el-upload__tip">mass_factor.csv</div>-->
            </el-upload>
          </el-form-item>
        </el-col>
        <!-- TE -->
        <el-col :span=12>
          <h5>{{ $t('Batch.PostBatch.TE.title') }}</h5>
          <el-radio-group v-model="radio" size="medium">
            <el-radio-button :label="$t('Batch.PostBatch.TE.auto_calculation')"></el-radio-button>
            <el-radio-button :label="$t('Batch.PostBatch.TE.manual_input')"></el-radio-button>
          </el-radio-group>
          <el-input v-model="batchInfo.TE_value"
                    :style="{display: elementShow,'margin-left':'10px','width':'40%'}"></el-input>
          <!--            <el-form-item label="TE.csv" label-width="70px" prop="file">-->
          <!--              <el-upload-->
          <!--                  ref="upload2"-->
          <!--                  :auto-upload="false"-->
          <!--                  :before-upload="handleBeforeUpload"-->
          <!--                  :file-list="fileList2"-->
          <!--                  :http-request="httpRequest"-->
          <!--                  :limit="2"-->
          <!--                  :multiple="false"-->
          <!--                  :on-change="handleChange2"-->
          <!--                  :on-exceed="handleExceed2"-->
          <!--                  :on-preview="handlePreview"-->
          <!--                  :on-remove="handleRemove2"-->
          <!--                  accept="text/csv"-->
          <!--                  action=""-->
          <!--                  class="upload-demo">-->
          <!--                <el-button slot="trigger" size="small" type="primary" plain>-->
          <!--                  {{ $t('Sample.common.sampleFile.selectBtn') }}-->
          <!--                </el-button>-->
          <!--                &lt;!&ndash; <div slot="tip" class="el-upload__tip">configuration_samples_mass.csv</div>&ndash;&gt;-->
          <!--              </el-upload>-->
          <!--            </el-form-item>-->
        </el-col>
        <el-col :span=24>
          <el-form-item style="margin-left: 10px">
            <el-button type="primary" @click="submitUpload()">{{ $t('Common.confirm.btn.create') }}</el-button>
            <el-button @click="cancel">{{ $t('Common.confirm.btn.cancel') }}</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import {postFormData} from "../../utils/api";

export default {
  name: 'PostBatch',
  components: {},
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
    return {
      fileList1: [],
      // fileList2: [],
      uploadData: "",
      batchInfo: {
        batchName: "",
        position: "",
        analysisType: "",
        sampleState: "",
        CpBase: "", CpExponent: "", V: "", T: "",
        dynamicItem: [],
        TE_value: '',
        TE_type: 'auto',
      },
      elementShow: 'none',
      radio: this.$t('Batch.PostBatch.TE.auto_calculation'),
      rules: {
        batchName: [{required: true, message: this.$t('Batch.PostBatch.basicInfo.batchName.rule'), trigger: "blur"}],
        position: [{required: true, message: this.$t('Batch.PostBatch.basicInfo.position.rule'), trigger: "blur"}],
        CpBase: [{required: true, validator: valiNumDotPass, trigger: "blur"}],
        CpExponent: [{required: true, validator: valiNumDotPass, trigger: "blur"}],
        V: [{required: true, validator: valiNumDotPass, trigger: "blur"}],
        T: [{required: true, validator: valiNumDotPass, trigger: "blur"}],
        analysisType: [{
          required: true,
          message: this.$t('Batch.PostBatch.basicInfo.analysisType.rule'),
          trigger: "blur"
        }],
        sampleState: [{
          required: true,
          message: this.$t('Batch.PostBatch.basicInfo.sampleState.rule'),
          trigger: "blur"
        }],
      },
      analysisTypeOptions: [
        {label: this.$t('Batch.common.analysisType.iteration'), value: '迭代法'},
        {label: this.$t('Batch.common.analysisType.poisson'), value: '泊松法'}],
      sampleStateOptions: [
        {label: this.$t('Sample.common.sampleState.solid'), value: '固体'},
        {label: this.$t('Sample.common.sampleState.liquid'), value: '液体'}],
    };
  },
  watch: {
    'radio': {
      handler(newValue, oldValue) {
        this.elementShow = newValue === this.$t('Batch.PostBatch.TE.manual_input') ? '' : 'none'
        this.batchInfo.TE_type = newValue === this.$t('Batch.PostBatch.TE.manual_input') ? 'manual' : 'auto'
      }
    }
  },
  computed: {
    Vi: function () {
      return this.batchInfo.V * (this.batchInfo.T / 60)
    },
    Cp: function () {
      return Math.pow(this.batchInfo.CpBase, this.batchInfo.CpExponent)
    }
  },
  activated() {
    this.clear();
  },
  methods: {
    // 增加物质条目
    addItem() {
      this.batchInfo.dynamicItem.push({sourceName: ""})
    },
    deleteItem(item, index) {
      this.batchInfo.dynamicItem.splice(index, 1)
    },
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
    async submitUpload() {
      // if (this.fileList1.length !== 1 || this.fileList2.length !== 1) {
      //   this.$message.error(this.$t('Sample.common.sampleFile.rule.empty'))
      //   return
      // }
      if (this.fileList1.length !== 1) {
        this.$message.error(this.$t('Sample.common.sampleFile.rule.empty'))
        return
      }
      await this.$refs.batchForm.validate((valid) => {
        if (valid) {
          // 上传TE校验
          let reg = /^[+-]?(0|([1-9]\d*))(\.\d+)?$/g;
          if (this.batchInfo.TE_type === 'manual' && !reg.test(this.batchInfo.TE_value)) {
            this.$message.error(this.$t('Common.numRule.num'))
            return
          }

          let uploadData = new FormData(); // 用FormData存放上传文件
          this.fileList1.forEach(file => {
            uploadData.append('calibration_curves', file.raw)
          })
          // this.fileList2.forEach(file => {
          //   uploadData.append('configuration_samples_mass', file.raw)
          // })
          uploadData.append('batchName', this.batchInfo.batchName)
          uploadData.append('experimentTime', this.batchInfo.experimentTime)
          uploadData.append('position', this.batchInfo.position)
          uploadData.append('analysisType', this.batchInfo.analysisType)
          uploadData.append('sampleState', this.batchInfo.sampleState)
          uploadData.append('sourceList', JSON.stringify(this.batchInfo.dynamicItem))
          uploadData.append('Cp', this.Cp)
          uploadData.append('V', this.batchInfo.V)
          uploadData.append('T', this.batchInfo.T)
          uploadData.append('Vi', this.Vi)
          uploadData.append('TE_type', this.batchInfo.TE_type)
          uploadData.append('TE_value', this.batchInfo.TE_value)

          // for (let [name, value] of uploadData) {
          //   console.log(name, '===>', value)
          // }

          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postFormData('/batch/postBatchInfo', uploadData).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              this.$message.success(resp.data.message)
              this.$router.push({path: "/batch/batchList"});
            } else {
              this.$message.error(resp.data.message)
            }
          })
        } else {
          return false;
        }
      });
    },
    // 界面相关
    cancel() {
      this.$confirm(this.$t('Common.confirm.msg.cancel'), this.$t('Common.confirm.title'), {
        confirmButtonText: this.$t('Common.confirm.btn.ok'),
        cancelButtonText: this.$t('Common.confirm.btn.cancel'),
        type: "warning",
      }).then(() => {
        this.$router.push({path: "/batch/batchList"});
      });
    },
    clear() {
      this.fileList1 = []
      // this.fileList2 = []
      this.uploadData = ""
      this.batchInfo = {
        batchName: "",
        experimentTime: "",
        position: "",
        analysisType: "",
        sampleState: "",
        Cp: "", V: "", T: "", Vi: this.Vi,
        dynamicItem: [{sourceName: ""},],
        TE_value: '',
        TE_type: 'auto'
      }
    },
  }
}
</script>

<style lang="less" scoped>
h4 {
  margin-top: 0;
  margin-bottom: 20px;
}
</style>