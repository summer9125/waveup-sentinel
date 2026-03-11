<template>
  <div class="events">
    <h2>📰 事件管理</h2>
    
    <!-- 搜索栏 -->
    <el-card style="margin-bottom: 20px;">
      <el-form :inline="true">
        <el-form-item label="关键词">
          <el-input placeholder="搜索关键词" style="width: 200px;" />
        </el-form-item>
        <el-form-item label="平台">
          <el-select placeholder="选择平台" style="width: 150px;">
            <el-option label="微信" value="wechat" />
            <el-option label="抖音" value="douyin" />
            <el-option label="微博" value="weibo" />
          </el-select>
        </el-form-item>
        <el-form-item label="情感">
          <el-select placeholder="选择情感" style="width: 120px;">
            <el-option label="正面" value="positive" />
            <el-option label="中性" value="neutral" />
            <el-option label="负面" value="negative" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary">搜索</el-button>
          <el-button>重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 事件列表 -->
    <el-card>
      <el-table :data="events" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="platform" label="平台" width="100" />
        <el-table-column prop="author" label="作者" width="150" />
        <el-table-column prop="sentiment_label" label="情感" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.sentiment === 'positive' ? 'success' : scope.row.sentiment === 'negative' ? 'danger' : 'info'">
              {{ scope.row.sentiment_label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="view_count" label="阅读数" width="100" />
        <el-table-column prop="publish_time" label="发布时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default>
            <el-button type="primary" size="small">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        layout="total, prev, pager, next"
        :total="100"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const events = ref([
  { title: 'WaveUP 新品发布会', platform: '微信', author: 'WaveUP 官方', sentiment: 'positive', sentiment_label: '正面', view_count: 10234, publish_time: '2026-03-08 13:00' },
  { title: '用户反馈产品体验', platform: '微博', author: '科技博主', sentiment: 'neutral', sentiment_label: '中性', view_count: 5678, publish_time: '2026-03-08 12:30' },
  { title: '竞品对比分析', platform: '抖音', author: '评测达人', sentiment: 'negative', sentiment_label: '负面', view_count: 23456, publish_time: '2026-03-08 12:00' },
])
</script>

<style scoped>
.events {
  padding: 20px;
}
</style>
