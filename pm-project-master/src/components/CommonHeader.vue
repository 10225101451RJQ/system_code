<template>
  <header>
    <div class="title">
      <h3>{{ $t('CommonHeader.title') }}</h3>
    </div>
    <el-menu :default-active="toIndex" class="menu"
             mode="horizontal"
             text-color="#ffffff">
      <el-menu-item v-for="item in menu" :key="item.path" :index="item.path" @click="clickMenu(item)">
        <i :class="'el-icon-' + item.icon" style="color: #FFFFFF"></i>
        <span slot="title">{{ item.label }}</span>
      </el-menu-item>
    </el-menu>
    <el-dropdown size="mini" trigger="click">
        <span>
          <img :src="userImg" class="userImg"/>
        </span>
      <el-dropdown-menu style="text-align: center">
        <el-dropdown-item common="b" @click.native="usrInfo">{{ $t('CommonHeader.dropdown.usrInfo') }}
        </el-dropdown-item>
        <el-dropdown-item common="b" @click.native="logOut">{{ $t('CommonHeader.dropdown.logout') }}</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <el-dialog :visible.sync='isShow' :title="$t('CommonHeader.dropdown.usrInfo')">
      <common-form ref='form' :form='formData'>
      </common-form>
      <div slot='footer' class='dialog-footer'>
        <el-button type='' @click='isShow = false'>{{ $t('Common.confirm.btn.cancel') }}</el-button>
        <el-button type='primary' @click='confirm'>{{ $t('Common.confirm.btn.ok') }}</el-button>
      </div>
    </el-dialog>
  </header>
</template>

<script>
import CommonForm from '@/components/CommonForm.vue';
import {getFormData, postFormData} from "../utils/api";

export default {
  name: "CommonHeader",
  components: {CommonForm},
  data() {
    return {
      isShow: false,
      activeIndex: '1',
      userImg: require('../../public/favicon.svg'),
      menu: [
        {
          path: '/batch',
          label: this.$t('CommonHeader.menu.batch'),
          icon: 's-grid',
        },
        {
          path: '/analysis',
          label: this.$t('CommonHeader.menu.analysis'),
          icon: 'data-board',
        }
      ],
      formValid: '',
      formData: {
        id: '',
        name: '',
        email: '',
        password: '',
        passwordConfirm: '',
      },
    };
  },
  methods: {
    clickMenu(item) {
      this.$router.push({path: item.path});
    },
    logOut() {
      this.$store.commit('clearToken')
      this.$router.push({name: 'login'})
    },
    usrInfo() {
      getFormData('/user/getInfo').then((resp) => {
        if (resp.data.code === 0) {
          this.isShow = true;
          resp.data.result['newPassword'] = ''
          resp.data.result['passwordConfirm'] = ''
          this.formData = JSON.parse(JSON.stringify(resp.data.result))  // 新对象，防止修改原值
        } else
          this.$message.error(resp.data.message)
      })
    },
    async confirm() {
      this.formValid = false
      await this.$bus.$emit('toFormValid', 'User')
      if (this.formValid) {
        var realFormData = JSON.parse(JSON.stringify(this.formData))  // 新对象，防止修改原值
        postFormData('/user/modifyInfo', {
          id: realFormData.id,
          email: realFormData.email,
          name: realFormData.name,
          password: this.$md5(realFormData.newPassword)
        }).then((resp) => {
          if (resp.data.code === 0) {
            this.$message({type: 'success', message: resp.data.message});
            this.isShow = false;
          } else this.$message({type: 'warning', message: resp.data.message});
        })
      }
    },
  },
  async mounted() {
    this.$bus.$on('returnFormValidUser', (data) => {
      this.formValid = data
    })
  },
  computed: {
    toIndex() {  // 根据路径绑定到对应的一级菜单，防止页面刷新重新跳回第一个
      return '/' + this.$route.path.split('/')[1];
    },
  }
}
</script>

<style lang="less" scoped>
header {
  display: flex;
  height: 100%;
  justify-content: flex-start;
  align-items: center;
}

.userImg {
  width: 45px;
  height: 45px;
  border-radius: 50%;
}

.title {
  margin-left: 10px;
  color: #FFFFFF;
  align-items: center;
}

.menu {
  margin-left: auto;
  background-color: transparent;
  margin-right: 10px;
}

.el-menu-item:hover {
  //outline: 0 !important;
  color: #3ab5b0 !important;
  font-weight: bold;
}

.el-menu-item.is-active {
  color: #fff !important;
  background: #3ab5b0 !important;
  font-weight: bold;
  border-bottom: #3ab5b0;
}
</style>