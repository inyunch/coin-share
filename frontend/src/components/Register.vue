<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" v-model="username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" required>
      </div>
      <div class="mb-3">
        <label for="name" class="form-label">Full Name</label>
        <input type="text" class="form-control" id="name" v-model="name" required>
      </div>
      <div class="mb-3">
        <label for="role" class="form-label">Role</label>
        <select class="form-select" id="role" v-model="role">
          <option value="user">User</option>
          <option value="group_admin">Group Admin</option>
          <option value="accountant">Accountant</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <p class="mt-3">Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const name = ref('')
    const role = ref('user')

    const register = async () => {
      try {
        await axios.post('http://localhost:8001/register', {
          username: username.value,
          password: password.value,
          name: name.value,
          role: role.value,
        })
        router.push('/login')
      } catch (error) {
        console.error('Registration failed:', error)
        alert('Registration failed. Please try again.')
      }
    }

    return { username, password, name, role, register }
  }
}
</script>