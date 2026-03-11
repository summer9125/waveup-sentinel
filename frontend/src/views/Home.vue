<template>
  <div class="home">
    <h2>📊 舆情概览</h2>
    
    <!-- 数据卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #409EFF;">📰</div>
            <div class="stat-info">
              <div class="stat-value">1,234</div>
              <div class="stat-label">今日事件</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #67C23A;">😊</div>
            <div class="stat-info">
              <div class="stat-value">85%</div>
              <div class="stat-label">正面舆情</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #E6A23C;">⚠️</div>
            <div class="stat-info">
              <div class="stat-value">12</div>
              <div class="stat-label">待处理告警</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #F56C6C;">🔥</div>
            <div class="stat-info">
              <div class="stat-value">3</div>
              <div class="stat-label">热门事件</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>舆情趋势</span>
            </div>
          </template>
          <div ref="trendChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>情感分布</span>
            </div>
          </template>
          <div ref="pieChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新事件 -->
    <el-card style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>最新事件</span>
          <el-button type="primary" size="small">查看更多</el-button>
        </div>
      </template>
      <el-table :data="recentEvents" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="platform" label="平台" width="100" />
        <el-table-column prop="sentiment" label="情感" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.sentiment === 'positive' ? 'success' : scope.row.sentiment === 'negative' ? 'danger' : 'info'">
              {{ scope.row.sentiment_label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_time" label="时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const trendChart = ref(null)
const pieChart = ref(null)

const recentEvents = ref([
  { title: 'WaveUP 新品发布会', platform: '微信', sentiment: 'positive', sentiment_label: '正面', publish_time: '2026-03-08 13:00' },
  { title: '用户反馈产品体验', platform: '微博', sentiment: 'neutral', sentiment_label: '中性', publish_time: '2026-03-08 12:30' },
  { title: '竞品对比分析', platform: '抖音', sentiment: 'negative', sentiment_label: '负面', publish_time: '2026-03-08 12:00' },
])

onMounted(() => {
  // 趋势图
  const trend = echarts.init(trendChart.value)
  trend.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
    },
    yAxis: { type: 'value' },
    series: [{
      data: [120, 200, 150, 80, 70, 110],
      type: 'line',
      smooth: true,
      areaStyle: {}
    }]
  })

  // 饼图
  const pie = echarts.init(pieChart.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '50%',
      data: [
        { value: 1048, name: '正面' },
        { value: 300, name: '中性' },
        { value: 135, name: '负面' }
      ]
    }]
  })
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
