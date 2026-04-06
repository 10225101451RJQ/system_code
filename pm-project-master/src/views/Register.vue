<template>
  <div class="container">
    <div class="main">
      <div class="main-left">
        <div class="top">
          <div class="top-img"><img src="../../public/title.svg"></div>
          <h2>{{ $t('Register.title') }}</h2>
          <h2>{{ $t('Register.title_2') }}</h2>
        </div>
        <div class="middle">
          <p class="mid-content">{{ $t('Register.introduction') }}</p>
        </div>
        <div class="bottom">
          <div class="bottom-content">
            <strong>SP-MAC@2.0 | <a @click="handleSetLanguage('zh')">简体中文</a>
              | <a @click="handleSetLanguage('en')">English</a></strong></div>
        </div>
      </div>
      <div class="main-right">
        <div class="title-reg">
          <h2>{{ $t('Register.registerBtn') }}</h2>
          <p>{{ $t('Register.toLogin_1') }}<a @click="login">&nbsp;{{ $t('Register.toLogin_2') }}</a></p>
        </div>
        <div class="inp-user">
          <el-form ref='form' :model='form' :rules='rules' label-width='100px' status-icon>
            <el-form-item :label='$t("Register.form.email.label")' label-width='85px' prop='email'>
              <el-input v-model='form.email' :placeholder='$t("Register.form.email.rule_1")'
                        auto-complete='off' type='input'></el-input>
            </el-form-item>
            <el-form-item :label='$t("Register.form.name.label")' label-width='85px' prop='name'
                          style="margin-top: 15px">
              <el-input v-model='form.name' :placeholder='$t("Register.form.name.rule_1")' auto-complete='off'
                        type='input'></el-input>
            </el-form-item>
            <el-form-item :label='$t("Register.form.password.label")' label-width='85px' prop='password'
                          style="margin-top: 15px">
              <el-input v-model='form.password' :placeholder='$t("Register.form.password.rule_1")' auto-complete='off'
                        type='password'></el-input>
            </el-form-item>
            <el-form-item :label='$t("Register.form.passwordConfirm.label")' label-width='85px' prop='passwordConfirm'
                          style="margin-top: 15px">
              <el-input v-model='form.passwordConfirm' :placeholder='$t("Register.form.passwordConfirm.rule_1")'
                        auto-complete='off' type='password'></el-input>
            </el-form-item>
            <el-form-item :label='$t("Register.form.captcha.label")' prop='captcha' label-width='85px'
                          style="margin-top: 15px">
              <el-input v-model='form.captcha' :placeholder='$t("Register.form.captcha.rule_1")'
                        auto-complete='off' type='input' style="float: left;width: 60%"></el-input>
              <el-button type="success" plain style="float: right;width: 35%;margin-left: 5%;height: 40px"
                         @click="toggleCaptchaButton" :class="{ 'disabled': isSending || isCounting }">
                <span v-if="isSending" class="f-size">{{ $t("Register.captcha.sending") }}</span>
                <span v-else-if="isCounting" class="f-size">{{ countdown }}s</span>
                <span v-else class="f-size">{{ $t("Register.captcha.send") }}</span>
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        <div class="confirm-user">
          <el-button type='primary' @click='register'>{{ $t('Register.registerBtn') }}</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {getFormData, postFormData} from '../utils/api';

export default {
  name: 'Register',
  data() {
    let valiEmailPass = (rule, value, callback) => {
      let reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/
      if (value === '') callback(new Error(this.$t("Register.form.email.rule_1")));
      else if (!reg.test(value)) callback(new Error(this.$t("Register.form.email.rule_2")));
      else callback();
    };
    let valiPasswordConfirm = (rule, value, callback) => {
      if (value === undefined || value === '') callback(new Error(this.$t("Register.form.passwordConfirm.rule_4")));
      else if (value !== this.form.password) callback(new Error(this.$t("Register.form.passwordConfirm.rule_5")));
      else callback();
    };
    let valiCaptchaConfirm = (rule, value, callback) => {
      if (value === undefined || value === '') callback(new Error(this.$t("Register.form.captcha.rule_2")));
      else if (value.length > 10) callback(new Error(this.$t("Register.form.captcha.rule_3")));
      else callback();
    };
    return {
      form: {},
      rules: {
        email: [{required: true, validator: valiEmailPass, trigger: 'blur'},],
        name: [
          {required: true, message: this.$t("Register.form.name.rule_1"), trigger: 'blur'},
          {min: 1, message: this.$t("Register.form.name.rule_2"), trigger: 'blur'},
          {max: 20, message: this.$t("Register.form.name.rule_3"), trigger: 'blur'}
        ],
        password: [
          {required: true, message: this.$t("Register.form.password.rule_1"), trigger: 'blur'},
          {min: 3, message: this.$t("Register.form.password.rule_2"), trigger: 'blur'},
          {max: 20, message: this.$t("Register.form.password.rule_3"), trigger: 'blur'}
        ],
        passwordConfirm: [
          {required: true, validator: valiPasswordConfirm, trigger: 'blur'},
        ],
        captcha: [
          {required: true, validator: valiCaptchaConfirm, trigger: 'blur'},
        ],
      },
      // 动态隐藏登录框
      isHidden: false,
      amHidden: false,
      //验证码变换
      isSending: false, // 是否正在发送验证码
      isCounting: false, // 是否正在倒计时
      countdown: 0, // 倒计时时间（秒），初始化为0，只在倒计时开始时设置为60
      countdownInterval: null, // 用于存储定时器的ID
    }
  },
  beforeDestroy() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval); // 组件销毁前清除定时器
    }
  },
  methods: {
    handleSetLanguage(lang) {
      this.$i18n.locale = lang
      this.$store.commit('setLanguage', lang)
      this.reload() // fix语言切换后，element-ui弹窗提示文字不能切换，必须强制刷新页面才能解决的bug
    },
    register: function () {
      this.$refs.form.validate((valid) => {
        if (valid) {
          postFormData('/user/register', {
            email: this.form.email,
            name: this.form.name,
            password: this.$md5(this.form.password),
            captcha: this.form.captcha,
          }).then((resp) => {
            if (resp.data.code === 0) {
              this.$confirm(this.$t('Register.toLogin_3'), this.$t('Common.confirm.title'), {
                confirmButtonText: this.$t('Common.confirm.btn.ok'),
                type: 'success',
              }).then(() => {
                this.$router.push('/login')
              }).catch(() => {
              });
            } else if (resp.data.code === 1) {
              this.$message.error(resp.data.message)
              this.form = {}
            }
          })
        } else return false
      });
    },
    login() {
      this.$router.push({name: 'login'})
    },
    // 验证码变换+发送验证码请求
    toggleCaptchaButton() {
      // 发送验证码请求
      // 检查是否正在发送请求或倒计时中
      if (this.isSending || this.isCounting) {
        this.$message.warning(this.$t("Register.captcha.countdown"));
        return // 提前返回，避免重复执行
      }
      getFormData('/user/getCaptcha', {email: this.form.email}).then((resp) => {
        if (resp.data.code === 0) {
          this.$message.success(this.$t("Register.captcha.alreadySend"));
        } else {
          this.$message({message: resp.data.message, type: 'error'})
        }
      })
      // 验证码变换
      if (!this.isSending && !this.isCounting) {
        this.isSending = true; // 开始发送验证码，设置为不可点击状态
        // 模拟发送验证码的过程
        setTimeout(() => {
          this.isSending = false; // 发送完成
          this.startCountdown(); // 调用倒计时
        }, 2500);
      }
    },
    startCountdown() {
      this.isCounting = true; // 开始倒计时
      this.countdown = 60; // 设置倒计时时间为60秒
      this.countdownInterval = setInterval(() => {
        this.countdown--; // 倒计时减1秒
        if (this.countdown <= 0) {
          this.stopCountdown(); // 倒计时结束，调用停止倒计时的方法
        }
      }, 1000); // 每秒更新一次倒计时时间
    },
    stopCountdown() {
      clearInterval(this.countdownInterval); // 清除定时器
      this.isCounting = false; // 倒计时结束
      this.countdown = 0; // 重置倒计时时间为0
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
  font-weight: bolder;
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
</style>