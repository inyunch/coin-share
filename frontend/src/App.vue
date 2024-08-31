<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light" v-if="isLoggedIn">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Coin Share</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/home">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage-group">Manage Group</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage-game">Manage Game</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view></router-view>
    </div>
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
    const isLoggedIn = computed(() => store.state.isLoggedIn)

    const logout = () => {
      store.commit('setLoggedIn', false)
      store.commit('setToken', null)
      router.push('/login')
    }

    return { isLoggedIn, logout }
  }
}
</script>