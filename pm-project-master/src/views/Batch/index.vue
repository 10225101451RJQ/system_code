<template>
  <div style="display: flex;height: 100%">
    <el-aside :style="{'width': width}" class="aside">
      <common-aside :menu="menu" style="margin-left: -20px"></common-aside>
    </el-aside>
    <el-main class="main">
      <el-card>
        <router-view></router-view>
      </el-card>
    </el-main>
  </div>
</template>

<script>
import CommonAside from '@/components/CommonAside';

export default {
  name: "index",
  components: {
    CommonAside
  },
  data() {
    return {
      menu: [
        {path: 'batchList', name: 'batch_batchList', label: this.$t('Batch.common.menu.batchList')},
        {path: 'postBatch', name: 'batch_postBatch', label: this.$t('Batch.common.menu.postBatch')},
        {path: 'recycleBin', name: 'batch_recycleBin', label: this.$t('Batch.common.menu.recycleBin')},
      ]
    }
  },
  computed: {
    width() {
      return this.$store.state.asideWidth
    }
  },
}
</script>

<style lang="less" scoped>
</style>