<template>
  <div class="container">
    <div class="main">
      <div class="main-left">
        <div class="top">
          <div class="top-img"><img src="../../public/title.svg"></div>
          <h2>{{ $t('Login.title') }}</h2>
          <h2>{{ $t('Login.title_2') }}</h2>
        </div>
        <div class="middle">
          <p class="mid-content">{{ $t('Login.introduction') }}</p>
        </div>
        <div class="bottom">
          <div class="bottom-content">
            <strong>SP-MAC@2.0 | <a @click="handleSetLanguage('zh')">简体中文</a>
              | <a @click="handleSetLanguage('en')">English</a></strong></div>
        </div>
      </div>
      <div class="main-right">
        <div class="title-reg">
          <h2>{{ $t('Login.loginBtn') }}</h2>
          <p>{{ $t('Login.toRegister_1') }}<a @click="register">&nbsp;{{ $t('Login.toRegister_2') }}</a></p>
        </div>
        <div class="inp-user">
          <el-form ref='form' :model='form' :rules='rules' label-width='100px' status-icon>
            <el-form-item :label='$t("Login.form.email.label")' label-width='85px' prop='email'>
              <el-input v-model='form.email' :placeholder='$t("Login.form.email.rule_1")'
                        auto-complete='off' type='input'></el-input>
            </el-form-item>
            <el-form-item :label='$t("Login.form.password.label")' label-width='85px' prop='password'
                          style="margin-top: 25px">
              <el-input v-model='form.password' :placeholder='$t("Login.form.password.rule_1")' auto-complete='off'
                        type='password'></el-input>
            </el-form-item>
          </el-form>
        </div>
        <div class="confirm-user">
          <el-button type='primary' @click='login'>{{ $t('Login.loginBtn') }}</el-button>
          <span><a @click="getBackPasswd">{{ $t('Login.getBackPasswd') }}</a></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {postFormData} from '../utils/api';

export default {
  name: 'Login',
  data() {
    let valiEmailPass = (rule, value, callback) => {
      let reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/
      if (value === '') callback(new Error(this.$t("Login.form.email.rule_1")));
      else if (!reg.test(value)) callback(new Error(this.$t("Login.form.email.rule_2")));
      else callback();
    };
    return {
      form: {
        email: '',
        password: ''
      },
      rules: {
        email: [{required: true, validator: valiEmailPass, trigger: 'blur'},],
        password: [
          {required: true, message: this.$t("Login.form.password.rule_1"), trigger: 'blur'},
          {min: 3, message: this.$t("Login.form.password.rule_2"), trigger: 'blur'},
          {max: 20, message: this.$t("Login.form.password.rule_3"), trigger: 'blur'}
        ],
      }
    }
  },
  methods: {
    handleSetLanguage(lang) {
      this.$i18n.locale = lang
      this.$store.commit('setLanguage', lang)
      this.reload() // fix语言切换后，element-ui弹窗提示文字不能切换，必须强制刷新页面才能解决的bug
    },
    login: function () {
      this.$refs.form.validate((valid) => {
        if (valid) {
          postFormData('/user/login', {
            email: this.form.email,
            password: this.$md5(this.form.password)
          }).then((resp) => {
            if (resp.data.code === 0) {
              this.$message({
                message: resp.data.message,
                type: 'success'
              })
              this.$store.commit('setToken', resp.data.result)
              this.$router.push({name: 'batch_batchList'})
            } else if (resp.data.code === 1) {
              this.$confirm(resp.data.message + ' ' + this.$t('Login.toRegister_3'), this.$t('Common.confirm.title'), {
                confirmButtonText: this.$t('Common.confirm.btn.ok'),
                type: 'error',
              }).then(() => {
                this.$router.push('/register')
              }).catch(() => {
              });
            }
          })
        } else return false;
      });
    },
    register: function () {
      this.$router.replace({name: 'register'})
    },
    getBackPasswd: function () {
      this.$router.replace({name: 'getBackPasswd'})
    },
  },
}
</script>

<style lang='less' scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.container {
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  height: 100%;
  width: 100%;
  background-size: cover;
  background: #eef2f5;
}

.main {
  width: 1000px;
  height: 564px;
  box-shadow: 0 10px 10px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  z-index: 1;
  display: flex;
}

.main .main-left {
  width: 500px;
  height: 564px;
  display: flex;
  position: relative;
  justify-content: space-around;
  flex-direction: column;
  background: linear-gradient(to bottom right, #3ab5b0 0%, #3d99be 31%, #56317a 100%);
  z-index: 2;
  padding: 80px 80px 50px;
}

.top {
  h2 {
    color: #FFFFFF;
    margin-top: 15px;
  }

  .top-img img {
    width: 250px;
  }
}

.middle {
  padding-top: 20px;
  padding-bottom: 80px;
}

.middle p {
  font-size: 14px;
  line-height: 25px;
}

.middle .mid-content {
  color: #fff;
  width: 340px;
  margin-top: 18px;
}

.bottom {
  width: 340px;
  border-top: 1px solid #ffffff;
  z-index: 5;
  padding-top: 15px;
}

.bottom-content {
  cursor: pointer;
  text-decoration: none;
  color: #fff;
  font-size: 15px;
  text-align: center;
  position: relative;
}

.main .main-right {
  width: 500px;
  height: 564px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  padding: 64px 70px 48px;
  color: #56317a;
}

.title-reg {
  display: flex;
  position: relative;
  padding-bottom: 40px;
}

.title-reg h2 {
  display: flex;
}

.title-reg > p {
  display: flex;
  margin-left: auto;
  margin-top: 10px;
  right: 0;
  font-size: 14px;
}

.title-reg > p a {
  text-decoration: none;
  color: #56317a;
}

.title-reg > p a:hover {
  color: #3ab5b0;
}

.confirm-user {
  margin-top: 20px;
}

.confirm-user button {
  width: 100%;
  height: 40px;
  letter-spacing: 15px;
  text-indent: 15px;
  font-size: 18px;
  border: 0;
  cursor: pointer;
  margin-top: 30px;
  margin-bottom: 20px;
}

.confirm-user span {
  display: block;
  text-align: center;
}

.confirm-user span > a {
  text-decoration: none;
  color: #56317a;
  font-size: 14px;
}

.confirm-user span > a:hover {
  color: #3ab5b0;
}
</style>