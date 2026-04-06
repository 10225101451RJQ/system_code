<template>
  <div class="common-table-multiple">
    <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange">
      <el-table-column
          type="selection"
          :width="multiTableWidth">
      </el-table-column>
      <el-table-column
          v-for="item in tableLabel"
          :key="item.prop"
          :label="item.label"
          min-width="25%"
          show-overflow-tooltip>
        <template slot-scope="scope"><span>{{ scope.row[item.prop] }}</span></template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "CommonTableMultiple",
  props: {
    tableData: Array,
    tableLabel: Array,
    function: String,
  },
  data() {
    return {
      multiTableWidth: '200%',
    }
  },
  watch: {
    'tableData': {
      handler() {
        if (this.tableData.length !== 0)
          this.multiTableWidth = '55'
        else this.multiTableWidth = '200%'
      }
    }
  },
  methods: {
    // 多选列表
    handleSelectionChange(val) {
      this.multipleSelection = val;
      this.$bus.$emit('returnSampleIdMultiple', {"function": this.function, "samples": this.multipleSelection});
    }
  }
}
</script>

<style lang="less" scoped>
.common-table-multiple {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>