<template>
  <el-form ref="form" :model="form" :rules='rules' label-width="100px">
    <el-form-item :label='$t("Register.form.email.label")' label-width='100px' prop='email'>
      <el-input v-model='form.email' :placeholder='$t("Register.form.email.rule_1")'
                auto-complete='off' type='input'></el-input>
    </el-form-item>
    <el-form-item :label='$t("Register.form.name.label")' label-width='100px' prop='name'
                  style="margin-top: 25px">
      <el-input v-model='form.name' :placeholder='$t("Register.form.name.rule_1")' auto-complete='off'
                type='input'></el-input>
    </el-form-item>
    <el-form-item :label='$t("Register.form.password.newLabel")' label-width='100px' prop='newPassword'
                  style="margin-top: 25px">
      <el-input v-model='form.newPassword' :placeholder='$t("Register.form.password.rule_1")' auto-complete='off'
                type='password'></el-input>
    </el-form-item>
    <el-form-item :label='$t("Register.form.passwordConfirm.label")' label-width='100px' prop='passwordConfirm'
                  style="margin-top: 25px">
      <el-input v-model='form.passwordConfirm' :placeholder='$t("Register.form.passwordConfirm.rule_1")'
                auto-complete='off'
                type='password'></el-input>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'CommonForm',
  props: {
    form: Object,       // 表单信息
  },
  methods: {
    resetForm() {
      this.$refs.form.resetFields()
    }
  },
  data() {
    let valiEmailPass = (rule, value, callback) => {
      let reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/
      if (value === '') callback(new Error(this.$t("Login.form.email.rule_1")));
      else if (!reg.test(value)) callback(new Error(this.$t("Login.form.email.rule_2")));
      else callback();
    };
    let valiNewPassword = (rule, value, callback) => {
      if (value !== undefined && value !== '' && value !== null) {
        if (value.length < 3) callback(new Error(this.$t("Register.form.password.rule_2")));
        else if (value.length > 20) callback(new Error(this.$t("Register.form.password.rule_3")));
        else callback();
      } else callback();
    };
    let valiPasswordConfirm = (rule, value, callback) => {
      if (this.form.newPassword !== undefined && this.form.newPassword !== '' && this.form.newPassword !== null) {
        if (value === undefined || value === '') callback(new Error(this.$t("Register.form.passwordConfirm.rule_4")));
        else if (value !== this.form.newPassword) callback(new Error(this.$t("Register.form.passwordConfirm.rule_5")));
        else callback();
      } else callback();
    };
    return {
      rules: {
        email: [{required: true, validator: valiEmailPass, trigger: 'blur'},],
        name: [
          {required: true, message: this.$t("Register.form.name.rule_1"), trigger: 'blur'},
          {min: 1, message: this.$t("Register.form.name.rule_2"), trigger: 'blur'},
          {max: 20, message: this.$t("Register.form.name.rule_3"), trigger: 'blur'}
        ],
        newPassword: [
          {required: false, validator: valiNewPassword, trigger: 'blur'},
        ],
        passwordConfirm: [
          {required: false, validator: valiPasswordConfirm, trigger: 'blur'},
        ]
      }
    }
  },
  mounted() {
    this.$bus.$on('toFormValid', (data) => {
      let event = 'returnFormValid' + data
      this.$nextTick(() => {
        this.$refs.form.validate((valid) => {
          this.$bus.$emit(event, valid)
        });
      });
    })
  },
  beforeDestroy() {
    this.$bus.$off('toFormValid')
  }
}
</script>

<style>
</style>