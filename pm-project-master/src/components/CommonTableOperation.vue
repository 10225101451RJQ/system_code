<template>
  <div class="common-table">
    <el-table :data="tableData" highlight-current-row>
      <el-table-column
          v-for="item in tableLabel"
          :key="item.prop"
          :label="item.label"
          min-width="25%"
          show-overflow-tooltip>
        <template slot-scope="scope">
          <span>{{ scope.row[item.prop] }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('CommonTableOperation.operation')" min-width="25%">
        <template slot-scope="scope">
          <el-button :style="{display: blueBtnShow}" plain size="mini" type="primary"
                     @click="handleEdit(scope.row)">{{ blueBtn }}
          </el-button>
          <el-button :style="{display: redBtnShow}" icon="el-icon-delete" plain size="mini" type="danger"
                     @click="handleDelete(scope.row)"></el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'CommonTableOperation',
  props: {
    tableData: Array,
    tableLabel: Array,
    config: Object,
    blueBtn: String,
    redBtn: String,
    blueBtnShow: String,
    redBtnShow: String
  },
  data() {
    return {}
  },
  methods: {
    // 给子组件绑定事件
    handleEdit(row) {
      this.$emit('edit', row)
    },
    handleDelete(row) {
      this.$emit('del', row)
    },
  },
}
</script>

<style lang="less" scoped>
</style>