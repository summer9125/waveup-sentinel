<template>
  <div class="settings">
    <h2>⚙️ 系统设置</h2>
    
    <el-tabs>
      <!-- 关键词设置 -->
      <el-tab-pane label="关键词管理">
        <el-card>
          <el-button type="primary" style="margin-bottom: 20px;">添加关键词</el-button>
          <el-table :data="keywords" style="width: 100%">
            <el-table-column prop="keyword" label="关键词" />
            <el-table-column prop="category" label="分类" width="120" />
            <el-table-column prop="weight" label="权重" width="80" />
            <el-table-column prop="is_active" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                  {{ scope.row.is_active ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default>
                <el-button type="primary" size="small">编辑</el-button>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <!-- API 配置 -->
      <el-tab-pane label="API 配置">
        <el-card>
          <el-form label-width="120px">
            <el-form-item label="新榜 API 密钥">
              <el-input placeholder="请输入新榜 API 密钥" />
            </el-form-item>
            <el-form-item label="微热点 API 密钥">
              <el-input placeholder="请输入微热点 API 密钥" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 通知设置 -->
      <el-tab-pane label="通知设置">
        <el-card>
          <el-form label-width="120px">
            <el-form-item label="飞书 Webhook">
              <el-input placeholder="飞书 Webhook URL" />
            </el-form-item>
            <el-form-item label="钉钉 Webhook">
              <el-input placeholder="钉钉 Webhook URL" />
            </el-form-item>
            <el-form-item label="告警级别">
              <el-checkbox-group>
                <el-checkbox label="critical">严重</el-checkbox>
                <el-checkbox label="high">高</el-checkbox>
                <el-checkbox label="medium">中</el-checkbox>
                <el-checkbox label="low">低</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const keywords = ref([
  { keyword: 'WaveUP', category: '品牌', weight: 10, is_active: true },
  { keyword: 'WaveUP 科技', category: '品牌', weight: 8, is_active: true },
  { keyword: '竞品 A', category: '竞品', weight: 5, is_active: true },
])
</script>

<style scoped>
.settings {
  padding: 20px;
}
</style>
