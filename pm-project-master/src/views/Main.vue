<template>
  <el-container style="height:100%">
    <el-header>
      <common-header></common-header>
    </el-header>
    <el-container style="background-color:#eef2f5;overflow-y: auto">
      <el-main>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </el-main>
    </el-container>
  </el-container>
</template>


<script>
import CommonHeader from '../components/CommonHeader.vue'

export default {
  name: 'Main',
  components: {
    CommonHeader
  },
  data() {
    return {}
  },
}
</script>

<style lang="less" scoped>
.el-header {
  background-image: linear-gradient(to left, #3ab5b0 0%, #3d99be 31%, #56317a 100%);
}

.el-main {
  padding-top: 0;
  overflow: auto;
}

</style>