<template>
  <!-- 指纹异同分析 -->
  <div>
    <div class="title">
      <h4>{{ $t('Analysis.FingerprintDiffSame.uploadFiles') }}</h4>
      <el-tag class="title-tag" type="success">{{ $t('Analysis.FingerprintDiffSame.tag') }}</el-tag>
    </div>
    <el-form ref="sampleForm" label-width="100px">
      <el-form-item :label="$t('Sample.common.sampleFile.label')" prop="file">
        <el-col :span="6">
          <el-upload
              ref="upload"
              :auto-upload="false"
              :file-list="fileList"
              :limit="1000"
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
        </el-col>
      </el-form-item>
    </el-form>
    <el-row>
      <el-radio-group v-model="radio">
        <el-radio-button :label="$t('Analysis.FingerprintDiffSame.allFingerprint')"></el-radio-button>
        <el-radio-button :label="$t('Analysis.FingerprintDiffSame.specificFingerprint')"></el-radio-button>
      </el-radio-group>
      <el-button type="primary" style="display: inline;margin-left: 10px" plain size="medium"
                 @click="submitUpload(radio)">
        {{ $t('Common.confirm.btn.download') }}
      </el-button>
    </el-row>
    <el-row :style="{display: elementShow}">
      <h5>{{ $t('Analysis.FingerprintDiffSame.filteredElement') }}</h5>
      <el-tag v-for='tag in elements' :key='tag' :disable-transitions='false' closable type='warning'
              @close='handleClose(tag)'>{{ tag }}
      </el-tag>
      <el-input v-if='inputElementVisible' ref='saveTagInput' v-model='inputElement'
                class='input-new-tag' size='small' style="width: auto" clearable
                :placeholder="$t('Common.numRule.empty')"
                @keyup.enter.native="handleInputConfirm"
                @blur="handleInputConfirm"></el-input>
      <el-button v-else class='button-new-tag' plain size='small' type='warning'
                 @click='showInput'>{{ $t('Analysis.FingerprintDiffSame.addFilteredElement') }}
      </el-button>
    </el-row>
  </div>
</template>

<script>
import {downloadCSV, postFormData, postJSON} from "../../utils/api";

export default {
  name: "FingerprintDiffSame",
  components: {},
  data() {
    return {
      elementTable: ['H', 'He',
        'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
        'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
        'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
        'Cs', 'Ba', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
        'Fr', 'Ra', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og',
        'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
        'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr'],
      inputElementVisible: false,
      inputElement: '',
      elementShow: 'none',
      radio: this.$t('Analysis.FingerprintDiffSame.allFingerprint'),
      elements: [],
      fileList: [],
    }
  },
  activated() {
    this.clear()
  },
  watch: {
    'radio': {
      handler(newValue, oldValue) {
        this.elementShow = newValue === this.$t('Analysis.FingerprintDiffSame.specificFingerprint') ? '' : 'none'
      }
    }
  },
  methods: {
    // 元素选择
    handleClose(tag) {
      this.elements.splice(this.elements.indexOf(tag), 1)
    },
    showInput() {
      this.inputElementVisible = true
      this.$nextTick(() => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },
    handleInputConfirm() {
      let inputElement = this.inputElement.trim()

      // 校验元素（无同位素）
      // if (this.elementTable.includes(inputElement))
      //   this.elements.push(inputElement);
      // else if (inputElement)
      //   this.$message.warning(this.$t('Analysis.FingerprintDiffSame.msg.wrongElement'))
      // 不校验元素
      if (inputElement !== '' && inputElement !== null && inputElement !== undefined)
        this.elements.push(inputElement);

      this.inputElementVisible = false
      this.inputElement = ''
    },
    // 文件上传
    handleChange(file, fileList) {
      this.fileList = fileList
    },
    handleRemove(file, fileList) {
      this.fileList = fileList;
    },
    handleExceed() {
      this.$message.warning(this.$t('Sample.common.sampleFile.rule.exceedFile_30'));
    },
    async submitUpload(radio) {
      let type = radio === this.$t('Analysis.FingerprintDiffSame.specificFingerprint') ? 'specific' : 'all'
      if (this.fileList.length === 0) {
        this.$message.error(this.$t('Sample.common.sampleFile.rule.leastFile_1'))
        return
      }
      if (this.elements.length === 0 && type === 'specific') {
        this.$message.error(this.$t('Analysis.FingerprintDiffSame.rule.leastElement_1'))
        return
      }
      // await this.$refs.sampleForm.validate((valid) => {
      //   if (valid) {
      let uploadData = new FormData(); // 用FormData存放上传文件
      this.fileList.forEach(file => {
        uploadData.append('sampleFile', file.raw)
      })
      uploadData.append('elements', this.elements.toString()) // 英文逗号,分隔字符串
      uploadData.append('type', type) // 下载文件类型
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      postFormData('/analysis/fingerprintDiffSame', uploadData).then((resp) => {
        loading.close();
        if (resp.data.code === 0) {
          this.$message.success(resp.data.message)
          this.downloadFile(resp.data.result.urls, type)
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
      // } else return false;
      // });
    },
    downloadFile(urls, type) {
      const loading = this.$loading({
        lock: true,
        text: this.$t('Common.loading.text'),
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      if (type === 'all') {
        postJSON('/download/url', {url: urls.all}).then((resp) => {
          downloadCSV(resp, 'all')
          loading.close()
        });
      } else if (type === 'specific') {
        postJSON('/download/url', {url: urls.filtered}).then((resp) => {
          downloadCSV(resp, 'selected-dominated ' + this.elements.toString())
        });
        postJSON('/download/url', {url: urls.unFiltered}).then((resp) => {
          downloadCSV(resp, 'selected-non-dominated ' + this.elements.toString())
        });
        loading.close()
      }
    },
    clear() {
      this.inputElementVisible = false
      this.inputElement = ''
      this.elementShow = 'none'
      this.radio = this.$t('Analysis.FingerprintDiffSame.allFingerprint')
      this.elements = []
      this.fileList = []
    },
  }
}
</script>

<style lang="less" scoped>
h4 {
  align-self: center;
  margin-top: 0;
}

.title {
  display: flex;
  justify-content: flex-start;
}

.title-tag {
  margin-top: -5px;
  //align-self: center;
  margin-left: 10px;
}

</style>