<template>
  <div class="settings-page">
    <div class="sidebar">
      <ul>
        <li @click="navigateTo('manage-group')" :class="{ active: isActive('manage-group') }">
          <i class="fas fa-users"></i> Manage Group
        </li>
        <li @click="navigateTo('manage-game')" :class="{ active: isActive('manage-game') }">
          <i class="fas fa-gamepad"></i> Manage Game
        </li>
      </ul>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'Settings',
  setup() {
    const router = useRouter()
    const route = useRoute()

    const navigateTo = (path) => {
      router.push(`/settings/${path}`)
    }

    const isActive = (path) => {
      return route.path.includes(path)
    }

    return { navigateTo, isActive }
  }
}
</script>

<style scoped>
.settings-page {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #f8f9fa;
  padding: 20px;
  border-right: 1px solid #ddd;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.sidebar li:hover, .sidebar li.active {
  background-color: #e9ecef;
}

.sidebar i {
  margin-right: 10px;
}

.content {
  flex-grow: 1;
  padding: 20px;
}
</style>