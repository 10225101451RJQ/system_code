<template>
  <div class="common-table-single">
    <el-table ref="singleTable"
              :data="tableData"
              highlight-current-row
              style="width: 100%"
              @current-change="handleCurrentChange">
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
  name: "CommonTableSingle",
  props: {
    tableData: Array,
    tableLabel: Array,
    function: String,
  },
  data() {
    return {}
  },
  methods: {
    // 单选列表
    setCurrent(row) {
      this.$refs.singleTable.setCurrentRow(row);
    },
    handleCurrentChange(val) {
      this.currentRow = val;
      this.$bus.$emit('returnSampleIdSingle', {"function": this.function, "sample": this.currentRow});
    }
  }
}
</script>

<style lang="less" scoped>
.common-table-single {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>