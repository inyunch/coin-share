<template>
  <div class="manage-game">
    <h2>Manage Games</h2>
    <form @submit.prevent="createGame" class="mb-4">
      <div class="form-group">
        <label for="gameName">Game Name</label>
        <input v-model="newGame.name" type="text" class="form-control" id="gameName" required>
      </div>
      <button type="submit" class="btn btn-primary mt-2">Create Game</button>
    </form>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <h3>Existing Games</h3>
    <ul class="list-group">
      <li v-for="game in games" :key="game.id" class="list-group-item d-flex justify-content-between align-items-center">
        {{ game.name }}
        <button @click="deleteGame(game.id)" class="btn btn-danger btn-sm">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'

export default {
  name: 'ManageGame',
  setup() {
    const store = useStore()
    const games = ref([])
    const newGame = ref({ name: '' })
    const error = ref(null)

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8001/games', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        games.value = response.data
        error.value = null
      } catch (err) {
        console.error('Failed to fetch games:', err)
        error.value = 'Failed to fetch games. Please try again.'
      }
    }

    const createGame = async () => {
      try {
        const response = await axios.post('http://localhost:8001/games', newGame.value, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        console.log('Game created:', response.data)
        newGame.value.name = ''
        error.value = null
        await fetchGames()
      } catch (err) {
        console.error('Failed to create game:', err)
        if (err.response) {
          if (typeof err.response.data === 'object' && err.response.data !== null) {
            error.value = `Failed to create game: ${JSON.stringify(err.response.data)}`
          } else {
            error.value = `Failed to create game: ${err.response.data || err.response.status}`
          }
        } else if (err.request) {
          error.value = 'Failed to create game: No response received from server'
        } else {
          error.value = `Failed to create game: ${err.message}`
        }
        console.log('Error value:', error.value)
      }
    }

    const deleteGame = async (gameId) => {
      if (confirm('Are you sure you want to delete this game?')) {
        try {
          await axios.delete(`http://localhost:8001/games/${gameId}`, {
            headers: { Authorization: `Bearer ${store.state.token}` }
          })
          error.value = null
          await fetchGames()
        } catch (err) {
          console.error('Failed to delete game:', err)
          error.value = `Failed to delete game: ${err.response && err.response.data ? JSON.stringify(err.response.data) : err.message}`
        }
      }
    }

    onMounted(fetchGames)

    return {
      games,
      newGame,
      createGame,
      deleteGame,
      error
    }
  }
}
</script>

<style scoped>
.manage-game {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1rem;
}

.list-group-item {
  margin-bottom: 0.5rem;
}
</style>