<template>
  <div>
    <h1>Manage Groups</h1>
    <form @submit.prevent="createGroup">
      <input v-model="groupName" placeholder="Group Name" required />
      <input v-model="groupCode" placeholder="Group Code" required />
      <select v-model="selectedGame">
        <option v-for="game in games" :key="game.id" :value="game.id">
          {{ game.name }}
        </option>
      </select>
      <button type="submit">Create Group</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      groupName: '',
      groupCode: '',
      selectedGame: null,
      games: [],
    };
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    async fetchGames() {
      const response = await axios.get('http://localhost:8000/games/');
      this.games = response.data;
    },
    async createGroup() {
      try {
        await axios.post('http://localhost:8000/groups/', {
          name: this.groupName,
          code: this.groupCode,
          game_id: this.selectedGame,
        });
        alert('Group created successfully!');
      } catch (error) {
        console.error('Error creating group:', error);
      }
    },
  },
};
</script>