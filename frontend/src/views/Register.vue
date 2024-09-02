<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <input v-model="username" type="text" class="form-control" id="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input v-model="password" type="password" class="form-control" id="password" required>
      </div>
      <div class="form-group">
        <label for="name">Name</label>
        <input v-model="name" type="text" class="form-control" id="name" required>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const name = ref('')
    const error = ref(null)

    const register = async () => {
      try {
        await axios.post('http://localhost:8000/users', {
          username: username.value,
          password: password.value,
          name: name.value
        })
        router.push('/login')
      } catch (err) {
        console.error('Registration error:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'An error occurred during registration'
      }
    }

    return { username, password, name, error, register }
  }
}
</script>

<style scoped>
.register {
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