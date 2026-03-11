<template>
  <div id="app">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="200px">
        <div class="logo">
          <h2>📊 WaveUP</h2>
          <p>舆情监控系统</p>
        </div>
        <el-menu
          :default-active="$route.path"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/">
            <el-icon><DataBoard /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/events">
            <el-icon><Document /></el-icon>
            <span>事件管理</span>
          </el-menu-item>
          <el-menu-item index="/analysis">
            <el-icon><TrendCharts /></el-icon>
            <span>情感分析</span>
          </el-menu-item>
          <el-menu-item index="/alerts">
            <el-icon><Bell /></el-icon>
            <span>告警中心</span>
          </el-menu-item>
          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main>
        <el-header>
          <div class="header-content">
            <h3>WaveUP Sentinel</h3>
            <div class="user-info">
              <el-tag type="success">运行中</el-tag>
              <span>开阳 ⭐</span>
            </div>
          </div>
        </el-header>
        
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { DataBoard, Document, TrendCharts, Bell, Setting } from '@element-plus/icons-vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo h2 {
  color: #409EFF;
  margin-bottom: 5px;
}

.logo p {
  color: #bfcbd9;
  font-size: 12px;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
