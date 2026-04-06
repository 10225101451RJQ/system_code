<template>
  <el-menu :default-active="toIndex" router>
    <el-menu-item
        v-for="item in menu" :key="item.path" :index="item.path">
      <span slot="title">{{ item.label }}</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'CommonAside',
  props: {
    menu: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {};
  },
  methods: {},
  computed: {
    toIndex() {  // 根据路径绑定到对应的二级菜单，防止页面刷新重新跳回第一个
      return this.$route.path.split('/')[2];
    }
  },
}
</script>

<style lang="less" scoped>
.el-menu {
  background-color: transparent;
}

.el-menu-item {
  font-size: medium;
}

.el-menu-item.is-active {
  font-weight: bold;
}
</style>

