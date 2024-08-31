<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input v-model="username" type="text" class="form-control" id="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input v-model="password" type="password" class="form-control" id="password" required>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <p>Don't have an account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const login = async () => {
      try {
        const success = await store.dispatch('login', {
          username: username.value,
          password: password.value
        })
        if (success) {
          router.push('/home')
        } else {
          alert('Login failed. Please check your credentials.')
        }
      } catch (error) {
        console.error('Login error:', error)
        alert('An error occurred during login. Please try again.')
      }
    }

    return { username, password, login }
  }
}
</script>