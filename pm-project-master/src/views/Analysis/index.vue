<template>
  <div style="display: flex;height: 100%">
    <el-aside class="aside" :style="{'width': width}">
      <h3 style="margin-bottom: 10px">{{ $t('Analysis.common.menu.basicAnalysis') }}</h3>
      <common-aside style="margin-left: -10px" :menu="menu_1"></common-aside>
      <h3 style="margin-top:25px;margin-bottom: 10px">{{ $t('Analysis.common.menu.fingerpintAnalysis') }}</h3>
      <common-aside style="margin-left: -10px" :menu="menu_2"></common-aside>
      <h3 style="margin-top:25px;margin-bottom: 10px">{{ $t('Analysis.common.menu.advancedAnalysis') }}</h3>
      <common-aside style="margin-left: -10px" :menu="menu_3"></common-aside>
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
      menu_1: [
        {
          path: 'detectionLimitCalculation',
          name: 'analysis_detectionLimitCalculation',
          label: this.$t('Analysis.common.menu.detectionLimitCalculation')
        },
        {path: 'particle', name: 'analysis_particle', label: this.$t('Analysis.common.menu.particle')},
        {path: 'supportX', name: 'analysis_supportX', label: this.$t('Analysis.common.menu.supportX')},
      ],
      menu_2: [
        {
          path: 'analysisSource',
          name: 'analysis_analysisSource',
          label: this.$t('Analysis.common.menu.analysisSource')
        },
        {
          path: 'analysisNotSource',
          name: 'analysis_analysisNotSource',
          label: this.$t('Analysis.common.menu.analysisNotSource')
        },
      ],
      menu_3: [
        {
          path: 'traceabilityAnalysis',
          name: 'analysis_traceabilityAnalysis',
          label: this.$t('Analysis.common.menu.traceabilityAnalysis')
        },
        {
          path: 'fingerprintDiffSame',
          name: 'analysis_fingerprintDiffSame',
          label: this.$t('Analysis.common.menu.fingerprintDiffSame')
        }
      ]
    }
  },
  computed: {
    width() {
      return this.$store.state.asideWidth
    }
  }
}
</script>

<style lang="less" scoped>
</style>