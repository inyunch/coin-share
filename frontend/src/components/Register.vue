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
        <label for="name">Full Name</label>
        <input v-model="name" type="text" class="form-control" id="name" required>
      </div>
      <div class="form-group">
        <label for="role">Role</label>
        <select v-model="role" class="form-control" id="role">
          <option value="user">User</option>
          <option value="group_admin">Group Admin</option>
          <option value="accountant">Accountant</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <p>Already have an account? <router-link to="/">Login</router-link></p>
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
          role: role.value
        })
        router.push('/')
      } catch (error) {
        console.error('Registration failed:', error)
        alert('Registration failed. Please try again.')
      }
    }

    return { username, password, name, role, register }
  }
}
</script>