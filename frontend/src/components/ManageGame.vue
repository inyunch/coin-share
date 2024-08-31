<template>
  <div class="manage-game">
    <h2>Manage Games</h2>
    <form @submit.prevent="createGame">
      <div class="form-group">
        <label for="gameName">Game Name</label>
        <input v-model="newGame.name" type="text" class="form-control" id="gameName" required>
      </div>
      <button type="submit" class="btn btn-primary">Create Game</button>
    </form>
    <h3>Existing Games</h3>
    <ul class="list-group">
      <li v-for="game in games" :key="game.id" class="list-group-item">
        {{ game.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ManageGame',
  setup() {
    const games = ref([])
    const newGame = ref({ name: '' })

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8001/games')
        games.value = response.data
      } catch (error) {
        console.error('Failed to fetch games:', error)
      }
    }

    const createGame = async () => {
      try {
        await axios.post('http://localhost:8001/games', newGame.value)
        newGame.value = { name: '' }
        await fetchGames()
      } catch (error) {
        console.error('Failed to create game:', error)
        alert('Failed to create game. Please try again.')
      }
    }

    onMounted(fetchGames)

    return { games, newGame, createGame }
  }
}
</script>