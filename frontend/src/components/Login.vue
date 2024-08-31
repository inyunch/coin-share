<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" v-model="username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <p class="mt-3">Don't have an account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const login = async () => {
      try {
        const response = await axios.post('http://localhost:8001/token', {
          username: username.value,
          password: password.value,
        })
        store.commit('setLoggedIn', true)
        store.commit('setToken', response.data.access_token)
        router.push('/home')
      } catch (error) {
        console.error('Login failed:', error)
        alert('Login failed. Please check your credentials.')
      }
    }

    return { username, password, login }
  }
}
</script>