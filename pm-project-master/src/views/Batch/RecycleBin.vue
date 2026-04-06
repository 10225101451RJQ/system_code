<template>
  <div>
    <!-- 展示列表 -->
    <div>
      <common-table-operation :blueBtn='$t("Batch.RecycleBin.tableOperation.blueBtn")' :tableData='batchList'
                              :tableLabel='tableLabel'
                              @changePage='search' @del='delBatch' @edit='editBatch'></common-table-operation>
    </div>
  </div>
</template>

<script>
import CommonTableOperation from '@/components/CommonTableOperation.vue'
import {getFormData, postFormData} from "../../utils/api";

export default {
  name: 'RecycleBin',
  components: {
    CommonTableOperation
  },
  data() {
    return {
      // 表格配置
      batchList: [],
      tableLabel: [
        {prop: 'batchName', label: this.$t('Batch.RecycleBin.tableOperation.options.batchName')},
        {prop: 'authorName', label: this.$t('Batch.RecycleBin.tableOperation.options.authorName')},
        {prop: 'position', label: this.$t('Batch.RecycleBin.tableOperation.options.position')},
        {prop: 'time', label: this.$t('Batch.RecycleBin.tableOperation.options.time')},
        {prop: 'remainingTime', label: this.$t('Batch.RecycleBin.tableOperation.options.remainingTime')},
      ],
    }
  },
  methods: {
    search: function () {
      getFormData('/delete/getDeleteBatchList', {}).then((resp) => {
        this.batchList = resp.data.result.batchList;
      })
    },
    editBatch(row) {
      this.$confirm(this.$t('Common.confirm.msg.recover'), this.$t('Common.confirm.title'), {
        confirmButtonText: this.$t('Common.confirm.btn.ok'),
        cancelButtonText: this.$t('Common.confirm.btn.cancel'),
        type: 'warning'
      }).then(() => {
        postFormData('/delete/restoreOneBatch', {id: row.id}).then((resp) => {
          if (resp.data.code === 0) {
            this.$message({type: 'success', message: resp.data.message});
            this.search()
          } else this.$message({type: 'warning', message: resp.data.message});
        })
      }).catch(() => {
        this.$message({type: 'info', message: this.$t('Common.message.cancelText')});
      });
    },
    delBatch(row) {
      this.$confirm(this.$t('Common.confirm.msg.delete'), this.$t('Common.confirm.title'), {
        confirmButtonText: this.$t('Common.confirm.btn.ok'),
        cancelButtonText: this.$t('Common.confirm.btn.cancel'),
        type: 'warning'
      }).then(() => {
        postFormData('/delete/deleteOneBatch', {id: row.id}).then((resp) => {
          if (resp.data.code === 0) {
            this.$message({type: 'success', message: resp.data.message});
            this.search()
          } else this.$message({type: 'warning', message: resp.data.message});
        })
      }).catch(() => {
        this.$message({type: 'info', message: this.$t('Common.message.cancelText')});
      });
    }
  },
  mounted() {
    this.search();
  },
}

</script>

<style lang="less" scoped>
.header-button {
  display: inline;
  float: left;
  margin-top: 5px;
}

.search {
  display: inline;
  float: right;
  margin-top: 5px;
}
</style>