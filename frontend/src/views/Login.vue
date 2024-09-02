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
    <p v-if="error" class="error">{{ error }}</p>
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
    const error = ref(null)

    const login = async () => {
      try {
        const success = await store.dispatch('login', {
          username: username.value,
          password: password.value
        })
        if (success) {
          router.push('/')
        } else {
          error.value = 'Invalid username or password'
        }
      } catch (err) {
        console.error('Login error:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'An error occurred during login'
      }
    }

    return { username, password, error, login }
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 1rem;
}
.error {
  color: red;
}
</style>