<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/token', {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/home'); // Redirect to home page on successful login
      } catch (error) {
        console.error('Error logging in:', error);
      }
    },
  },
};
</script>