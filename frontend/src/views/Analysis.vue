<template>
  <div class="analysis">
    <h2>📈 情感分析</h2>
    
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>情感趋势</template>
          <div ref="trendChart" style="height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>情感分布</template>
          <div ref="pieChart" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const trendChart = ref(null)
const pieChart = ref(null)

onMounted(() => {
  const trend = echarts.init(trendChart.value)
  trend.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['正面', '中性', '负面'] },
    xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
    yAxis: { type: 'value' },
    series: [
      { name: '正面', type: 'line', data: [120, 132, 101, 134, 90, 230, 210], smooth: true },
      { name: '中性', type: 'line', data: [220, 182, 191, 234, 290, 330, 310], smooth: true },
      { name: '负面', type: 'line', data: [150, 232, 201, 154, 190, 330, 410], smooth: true }
    ]
  })

  const pie = echarts.init(pieChart.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
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
.analysis {
  padding: 20px;
}
</style>
