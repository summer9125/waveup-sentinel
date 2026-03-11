<template>
  <div class="alerts">
    <h2>🔔 告警中心</h2>
    
    <el-card>
      <el-table :data="alerts" style="width: 100%">
        <el-table-column prop="level" label="级别" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.level === 'critical' ? 'danger' : scope.row.level === 'high' ? 'warning' : 'info'">
              {{ scope.row.level_label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="event_title" label="关联事件" />
        <el-table-column prop="channel" label="通知渠道" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'sent' ? 'success' : scope.row.status === 'pending' ? 'warning' : 'danger'">
              {{ scope.row.status_label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default>
            <el-button type="primary" size="small">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const alerts = ref([
  { level: 'critical', level_label: '严重', title: '重大负面舆情', event_title: '产品质量问题投诉', channel: '飞书', status: 'sent', status_label: '已发送', created_at: '2026-03-08 13:00' },
  { level: 'high', level_label: '高', title: '热度快速上升', event_title: '新品发布会', channel: '钉钉', status: 'pending', status_label: '待发送', created_at: '2026-03-08 12:30' },
])
</script>

<style scoped>
.alerts {
  padding: 20px;
}
</style>
