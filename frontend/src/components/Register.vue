<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="register">
      <input v-model="name" placeholder="Name" required />
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="groupCode" placeholder="Group Code" required />
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',
      username: '',
      password: '',
      groupCode: '',
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('http://localhost:8000/register', {
          name: this.name,
          username: this.username,
          password: this.password,
          group_code: this.groupCode,
        });
        alert('Registration successful!');
        this.$router.push('/');
      } catch (error) {
        console.error('Error registering:', error);
      }
    },
  },
};
</script>