<template>
  <div>
    <el-form :inline="true">
      <el-form-item :label="$t('Batch.BatchList.search.type')">
        <el-select v-model="form.searchType" :placeholder="$t('Batch.BatchList.search.rule_1')" clearable
                   style="width: 200px">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :style="{display: inputShow}">
        <el-input v-model="form.input" :placeholder="$t('Batch.BatchList.search.rule_2')"
                  style="width: 200px"></el-input>
      </el-form-item>
      <el-form-item :style="{display: datePickerShow}">
        <el-date-picker
            v-model="form.input"
            :end-placeholder="$t('Batch.BatchList.search.endDate')"
            :range-separator="$t('Batch.BatchList.search.toDate')"
            :start-placeholder="$t('Batch.BatchList.search.startDate')"
            type="daterange"
            value-format="yyyy-MM-dd">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button icon="el-icon-search" type="success" @click="search(form.searchType,form.input,currentPage)">
          {{ $t('Batch.BatchList.search.label') }}
        </el-button>
      </el-form-item>
    </el-form>
    <!-- 展示列表 -->
    <div>
      <common-table-operation :blueBtn="$t('Batch.BatchList.tableOperation.blueBtn')" :tableData='batchList'
                              :tableLabel='tableLabel'
                              @changePage='search(form.searchType,form.input,currentPage)' @del='delBatch'
                              @edit='editBatch'></common-table-operation>
    </div>
    <!-- 底部跳转 -->
    <div style="text-align: center;margin-top: 10px">
      <el-pagination :current-page.sync="currentPage" :page-count="totalPages" :page-size="pageSize"
                     :pager-count="5" background
                     layout="prev, pager, next, jumper" @current-change="handleCurrentChange">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import CommonTableOperation from '@/components/CommonTableOperation.vue'
import {postFormData} from "../../utils/api";
import Cookie from "js-cookie";

export default {
  name: 'BatchList',
  components: {
    CommonTableOperation
  },
  data() {
    return {
      inputShow: "",
      datePickerShow: "none",
      // 搜索配置
      form: {
        searchType: '',
        input: ''
      },
      options: [
        {value: '批次名', label: this.$t('Batch.BatchList.search.options.batchName')},
        {value: '创建时间', label: this.$t('Batch.BatchList.search.options.time')}],
      // 表格配置
      batchList: [],
      tableLabel: [
        {prop: 'batchName', label: this.$t('Batch.BatchList.tableOperation.options.batchName')},
        {prop: 'sampleState', label: this.$t('Batch.BatchList.tableOperation.options.sampleState')},
        {prop: 'position', label: this.$t('Batch.BatchList.tableOperation.options.position')},
        {prop: 'authorName', label: this.$t('Batch.BatchList.tableOperation.options.authorName')},
        {prop: 'time', label: this.$t('Batch.BatchList.tableOperation.options.time')},
      ],
      // 翻页配置
      pageSize: 10,
      totalPages: 1,
      currentPage: 1,
    }
  },
  watch: {
    'form.searchType': {
      handler(newValue, oldValue) {
        this.form.input = ''
        if (newValue === '创建时间') {
          this.inputShow = 'none'
          this.datePickerShow = ''
        } else {
          this.inputShow = ''
          this.datePickerShow = 'none'
        }
      }
    }
  },
  methods: {
    search: function (searchType, input, currentPage) {
      postFormData('/batch/getMyBatchList', {
        searchType: searchType,
        input: input.toString(),
        currentPage: currentPage
      }).then((resp) => {
        this.batchList = resp.data.result.batchList
        for (let i in this.batchList) {
          let state = this.batchList[i].sampleState
          if (Cookie.get('language') === 'en') {
            if (state === '固体')
              this.batchList[i].sampleState = 'solid'
            else this.batchList[i].sampleState = 'liquid'
          }
        }
        this.totalPages = resp.data.result.totalPages
        this.currentPage = resp.data.result.currentPage
      })
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage
      this.search(this.form.searchType, this.form.input, this.currentPage)
    },
    editBatch(row) {
      this.$router.push({name: 'batch_detailBatch', query: {id: row.id}})
    },
    delBatch(row) {
      this.$confirm(this.$t('Common.confirm.msg.recycleBin'), this.$t('Common.confirm.title'), {
        confirmButtonText: this.$t('Common.confirm.btn.ok'),
        cancelButtonText: this.$t('Common.confirm.btn.cancel'),
        type: 'warning'
      }).then(() => {
        postFormData('/delete/addOneBatch', {id: row.id}).then((resp) => {
          if (resp.data.code === 0) {
            this.$message({type: 'success', message: resp.data.message});
            this.search(this.form.searchType, this.form.input, this.currentPage)
          } else this.$message({type: 'warning', message: resp.data.message});
        })
      }).catch(() => {
        this.$message({type: 'info', message: this.$t('Common.message.cancelText')});
      });
    }
  },
  mounted() {
    this.currentPage = 1
    this.search('', '', this.currentPage)
  },
}
</script>

<style lang="less" scoped>
</style>