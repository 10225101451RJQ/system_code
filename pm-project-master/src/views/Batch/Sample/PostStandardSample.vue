<template>
  <div>
    <h3>{{ $t('Sample.PostStandardSample.title') }}</h3>
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
            {{ $t('Sample.PostStandardSample.sampleProperty') }}
          </el-form-item>
        </el-col>
      </el-row>
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
      <el-button type="primary" @click="submitUpload">{{ $t('Sample.common.sampleFile.uploadBtn') }}</el-button>
      <el-button @click="cancel">{{ $t('Common.confirm.btn.cancel') }}</el-button>
    </el-form>
  </div>
</template>

<script>
import {postFormData} from '../../../utils/api';

export default {
  name: 'PostStandardSample',
  data() {
    return {
      placeHolder: "",
      sampleInfo: {
        batchId: "",
        batchName: "",
        sampleState: "",
        sampleProperty: this.$t('Sample.PostStandardSample.sampleProperty'),
      },
      fileList: [],
    }
  },
  watch: {},
  async activated() {
    this.clear()
    this.sampleInfo.batchId = this.$route.query.batchId;
    this.sampleInfo.batchName = this.$route.query.batchName;
    this.sampleInfo.sampleState = this.$route.query.sampleState;
  },
  methods: {
    changeValue(e) {
      this.$forceUpdate()
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

          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postFormData('/sample/postStandardSample', uploadData).then((resp) => {
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
        position: "",
        batchName: "",
        sampleState: "",
        sampleProperty: "",
      }
      this.fileList = []
    },
  }
}
</script>

<style lang="less" scoped>
h3 {
  margin-top: 0;
}
</style>