<template>
  <div>
    <h3>{{ $t('Sample.PostConfigSample.title') }}</h3>
    <el-form ref="sampleForm" :model="sampleInfo" :rules="rules" label-width="100px">
      <el-row>
        <el-col :span=4>
          <el-form-item :label="$t('Sample.common.batchName')" prop="batch">
            {{ sampleInfo.batchName }}
          </el-form-item>
        </el-col>
        <el-col :span=4>
          <el-form-item :label="$t('Sample.common.sampleState.label')" prop="sampleState">
            {{ sampleInfo.sampleState }}
          </el-form-item>
        </el-col>
        <el-col :span=4>
          <el-form-item :label="$t('Sample.common.sampleProperty')">
            {{ $t('Sample.PostConfigSample.sampleProperty') }}
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span=6>
          <el-form-item :label="$t('Sample.common.params.Df.label')" label-width="100px" prop="Df">
            <el-input v-model="sampleInfo.Df" :placeholder="$t('Sample.common.params.Df.rule')"
                      style="width: 80%"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Sample.common.params.Vf.label')" :style="{display: stateShow}" label-width="130px"
                        prop="Vf">
            <el-input v-model="sampleInfo.Vf" :placeholder="$t('Sample.common.params.Vf.rule')"
                      style="width: 80%"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span=6>
          <el-form-item :label="$t('Sample.common.params.m.label')" :style="{display: stateShow}" label-width="130px"
                        prop="m">
            <el-input v-model="sampleInfo.m" :placeholder="$t('Sample.common.params.m.rule')"
                      style="width: 80%"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <h4>{{ $t('Sample.PostConfigSample.sampleMgMl') }}</h4>
      <!--      表单校验：prop和v-model的值要相同-->
      <div v-for="(item,index) in sampleInfo.dynamicItem" :key="index" style="display: flex">
        <el-form-item :label="item.sourceName"
                      :prop="'dynamicItem.'+index+'.sourceMass'"
                      :rules="{required:true, validator:vali, trigger:'blur'}">
          <el-input v-model="item.sourceMass" :placeholder="placeHolder"></el-input>
        </el-form-item>
      </div>
      <el-form-item :label="$t('Sample.common.sampleFile.label')" prop="file">
        <el-upload
            ref="upload"
            :auto-upload="false"
            :file-list="fileList"
            :http-request="httpRequest"
            :limit="2"
            :multiple="false"
            :on-change="handleChange"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            accept="text/csv"
            action=""
            class="upload-demo">
          <el-button slot="trigger" plain size="small" type="primary">
            {{ $t('Sample.common.sampleFile.selectBtn') }}
          </el-button>
          <div slot="tip" class="el-upload__tip">{{ $t('Sample.common.sampleFile.tip') }}</div>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitUpload">{{ $t('Sample.common.sampleFile.uploadBtn') }}</el-button>
        <el-button @click="cancel">{{ $t('Common.confirm.btn.cancel') }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {postFormData, postJSON} from '../../../utils/api';

export default {
  name: 'PostConfigSample',
  data() {
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
      placeHolder: "",
      stateShow: "none",
      sampleInfo: {
        batchId: "",
        batchName: "",
        sampleState: "",
        sampleProperty: this.$t('Sample.PostConfigSample.sampleProperty'),
        dynamicItem: [],
        sourceList: [],
        Vf: "", Df: "", m: ""
      },
      fileList: [],
      rules: {
        Vf: [{required: true, trigger: "blur", validator: valiNumDotPass}],
        Df: [{required: true, trigger: "blur", validator: valiNumDotPass}],
        m: [{required: true, trigger: "blur", validator: valiNumDotPass}],
      },
      vali: valiNumDotPass
    }
  },
  watch: {
    'sampleInfo.sampleState': {
      handler() {
        if (this.sampleInfo.sampleState === '固体' || this.sampleInfo.sampleState === 'solid')
          this.stateShow = ''
        else if (this.sampleInfo.sampleState === '液体' ||  this.sampleInfo.sampleState === 'liquid') {
          this.stateShow = 'none'
          this.sampleInfo.Vf = '-1'
          this.sampleInfo.m = '-1'
        }
      }
    },
  },
  activated() {
    this.clear()
    this.sampleInfo.batchId = this.$route.query.batchId;
    this.sampleInfo.batchName = this.$route.query.batchName;
    this.sampleInfo.sampleState = this.$route.query.sampleState;
    this.getBatchInfo();
  },
  methods: {
    async getBatchInfo() {
      await postJSON('/batch/getBatchInfo', {batchId: this.$route.query.batchId}).then((resp) => {
        if (resp.data.code === 0) {
          this.sampleInfo.dynamicItem = []
          this.sampleInfo.sourceList = resp.data.result.batchInfo.sourceList
          for (let i = 0; i < resp.data.result.batchInfo.sourceList.length; i++) {
            this.sampleInfo.dynamicItem.push({
              sourceName: resp.data.result.batchInfo.sourceList[i].label,
              sourceMass: "",
            })
          }
        } else {
          this.$message.warning(resp.data.message)
        }
      });
    },
    // 文件上传
    httpRequest(param) { // submitUpload重复调用httpRequest，达到效果
    },
    handleBeforeUpload(file) {
      if (this.fileList.length !== 1)
        this.$message.error(this.$t('Sample.common.sampleFile.rule.exceedFile_1'));
    },
    handleSuccess(res, file) {
    },
    handleChange(file, fileList) {
      if (this.$refs.upload.uploadFiles.length > 1)
        this.$refs.upload.uploadFiles.shift()
      if (this.$refs.upload.uploadFiles.length > 0)
        this.fileList = this.$refs.upload.uploadFiles
    },
    handleRemove(file, fileList) {
      this.fileList = fileList;
    },
    handlePreview(file) {
    },
    handleExceed() {
      this.$message.error(this.$t('Sample.common.sampleFile.rule.exceedFile_1'));
    },
    async submitUpload() {
      if (this.fileList.length !== 1) {
        this.$message.error(this.$t('Sample.common.sampleFile.rule.empty'))
        return
      }
      await this.$refs.sampleForm.validate((valid) => {
        if (valid) {
          let uploadData = new FormData(); // 用FormData存放上传文件
          this.fileList.forEach(file => {
            uploadData.append('sampleFile', file.raw)
          })
          uploadData.append('batchId', this.sampleInfo.batchId)
          uploadData.append('sourceList', JSON.stringify(this.sampleInfo.dynamicItem))
          uploadData.append('Vf', this.sampleInfo.Vf)
          uploadData.append('Df', this.sampleInfo.Df)
          uploadData.append('m', this.sampleInfo.m)

          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postFormData('/sample/postConfigSample', uploadData).then((resp) => {
            loading.close();
            if (resp.data.code === 0) {
              this.$message.success(resp.data.message)
              this.$router.back()
            } else {
              this.$message.error(resp.data.message)
            }
          })
        } else return false;
      });
    },
    // 界面相关
    cancel() {
      this.$confirm(this.$t('Common.confirm.msg.cancel'), this.$t('Common.confirm.title'), {
        confirmButtonText: this.$t('Common.confirm.btn.ok'),
        cancelButtonText: this.$t('Common.confirm.btn.cancel'),
        type: "warning",
      }).then(() => {
        this.$router.back();
      });
    },
    clear() {
      this.sampleInfo = {
        batchId: "",
        batchName: "",
        sampleState: "",
        sampleProperty: "",
        dynamicItem: [],
        sourceList: [],
        Vf: "", Df: "", m: ""
      }
      this.fileList = []
    },
    resolveBug() {
      this.$forceUpdate();
    }
  }
}
</script>

<style lang="less" scoped>
h4 {
  margin-top: 0;
}

h3 {
  margin-top: 0;
}
</style>