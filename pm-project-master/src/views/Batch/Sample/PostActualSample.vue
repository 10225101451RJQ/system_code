<template>
  <div>
    <h3>{{ $t('Sample.PostActualSample.title') }}</h3>
    <el-form ref="sampleForm" :model="sampleInfo" :rules="rules" label-width="100px">
      <el-row>
        <el-col :span=4>
          <el-form-item :label="$t('Sample.common.batchName')" prop="batchName">
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
            {{ $t('Sample.PostActualSample.sampleProperty') }}
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
      <el-row>
        <el-col :span="6">
          <el-form-item :label="$t('Sample.common.sampleFile.label')" prop="file">
            <el-upload
                ref="upload"
                :auto-upload="false"
                :file-list="fileList"
                :limit="10"
                :multiple="true"
                :on-change="handleChange"
                :on-exceed="handleExceed"
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
        </el-col>
      </el-row>
      <el-form-item>
        <el-button type="primary" @click="submitUpload">{{ $t('Sample.common.sampleFile.uploadBtn') }}</el-button>
        <el-button @click="cancel">{{ $t('Common.confirm.btn.cancel') }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {postFormData} from '../../../utils/api';

export default {
  name: 'PostActualSample',
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
      stateShow: "none",
      sampleInfo: {
        batchId: "",
        batchName: "",
        sampleState: "",
        sampleProperty: this.$t('Sample.PostActualSample.sampleProperty'),
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
        if (this.sampleInfo.sampleState === '固体' ||  this.sampleInfo.sampleState === 'solid')
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
  },
  methods: {
    // 文件上传
    handleChange(file, fileList) {
      this.fileList = fileList
    },
    handleRemove(file, fileList) {
      this.fileList = fileList;
    },
    handleExceed() {
      this.$message.warning(this.$t('Sample.common.sampleFile.rule.exceedFile_10'));
    },
    async submitUpload() {
      if (this.fileList.length === 0) {
        this.$message.error(this.$t('Sample.common.sampleFile.rule.leastFile_1'))
        return
      }
      await this.$refs.sampleForm.validate((valid) => {
        if (valid) {
          let uploadData = new FormData(); // 用FormData存放上传文件
          this.fileList.forEach(file => {
            uploadData.append('sampleFile', file.raw)
          })
          uploadData.append('batchId', this.sampleInfo.batchId)
          uploadData.append('Vf', this.sampleInfo.Vf)
          uploadData.append('Df', this.sampleInfo.Df)
          uploadData.append('m', this.sampleInfo.m)

          const loading = this.$loading({
            lock: true,
            text: this.$t('Common.loading.text'),
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          postFormData('/sample/postActualSample', uploadData).then((resp) => {
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
h3 {
  margin-top: 0;
}
</style>