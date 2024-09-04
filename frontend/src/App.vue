<template>
  <div id="app">
    <nav class="navbar" v-if="isLoggedIn">
      <div class="navbar-container">
        <router-link to="/" class="navbar-logo">
          <img src="path/to/your/logo.png" alt="Coin Share Logo" />
        </router-link>
        <ul class="navbar-menu">
          <li class="navbar-item">
            <router-link to="/home" class="navbar-link">Home</router-link>
          </li>
          <li class="navbar-item">
            <router-link to="/manage-group" class="navbar-link">Manage Group</router-link>
          </li>
          <li class="navbar-item">
            <router-link to="/manage-game" class="navbar-link">Manage Game</router-link>
          </li>
        </ul>
        <div class="navbar-icons">
          <router-link to="/settings" class="navbar-icon">
            <i class="fas fa-cog"></i> Settings
          </router-link>
          <a href="#" @click.prevent="logout" class="navbar-icon">
            <i class="fas fa-sign-out-alt"></i> Logout
          </a>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()
    const isLoggedIn = computed(() => store.getters.isLoggedIn)

    const logout = () => {
      store.dispatch('logout')
      router.push('/login')
    }

    return { isLoggedIn, logout }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.navbar-logo img {
  height: 40px;
}

.navbar-menu {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0;
}

.navbar-item {
  margin-left: 20px;
}

.navbar-link {
  text-decoration: none;
  color: #333;
  font-weight: bold;
  transition: color 0.3s;
}

.navbar-link:hover, .navbar-link.router-link-active {
  color: #007bff;
}

.navbar-icons {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.navbar-icon {
  margin-left: 20px;
  color: #333;
  text-decoration: none;
  transition: color 0.3s;
}

.navbar-icon:hover {
  color: #007bff;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    align-items: flex-start;
  }

  .navbar-menu {
    flex-direction: column;
    width: 100%;
    margin-top: 10px;
  }

  .navbar-item {
    margin-left: 0;
    margin-bottom: 10px;
  }

  .navbar-icons {
    width: 100%;
    justify-content: flex-end;
    margin-top: 10px;
  }
}
</style>