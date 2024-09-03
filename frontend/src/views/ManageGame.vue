<template>
  <div class="manage-game">
    <h2>Manage Games</h2>
    <form @submit.prevent="createGame" class="mb-4" v-if="isAdmin">
      <div class="form-group">
        <label for="gameName">Game Name</label>
        <input v-model="newGame.name" type="text" class="form-control" id="gameName" required>
      </div>
      <button type="submit" class="btn btn-primary mt-2">Create Game</button>
    </form>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div v-if="message" class="alert alert-success" role="alert">
      {{ message }}
    </div>
    <h3>Existing Games</h3>
    <ul class="list-group">
      <li v-for="game in games" :key="game.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span v-if="!isEditing(game.id)">{{ game.name }}</span>
        <input v-else v-model="editGameName" type="text" class="form-control" />
        <div>
          <button @click="startEditing(game)" class="btn btn-secondary btn-sm" v-if="isAdmin && !isEditing(game.id)">Edit</button>
          <button @click="updateGame(game.id)" class="btn btn-success btn-sm" v-if="isAdmin && isEditing(game.id)">Save</button>
          <button @click="cancelEditing" class="btn btn-warning btn-sm" v-if="isAdmin && isEditing(game.id)">Cancel</button>
          <button @click="deleteGame(game.id)" class="btn btn-danger btn-sm" v-if="isAdmin">Delete</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'

export default {
  name: 'ManageGame',
  setup() {
    const store = useStore()
    const games = ref([])
    const newGame = ref({ name: '' })
    const editGameName = ref('')
    const editingGameId = ref(null)
    const error = ref(null)
    const message = ref(null)

    const isAdmin = computed(() => store.state.user && store.state.user.role === 'admin')

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8000/games', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        games.value = response.data
        error.value = null
      } catch (err) {
        console.error('Failed to fetch games:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to fetch games. Please try again.'
      }
    }

    const createGame = async () => {
      if (!isAdmin.value) {
        error.value = 'You do not have permission to create games.'
        return
      }
      try {
        const response = await axios.post('http://localhost:8000/games', newGame.value, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        console.log('Game created:', response.data)
        message.value = 'Game created successfully!'
        newGame.value.name = ''
        error.value = null
        await fetchGames()
      } catch (err) {
        console.error('Failed to create game:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to create game. Please try again.'
        message.value = null
      }
    }

    const startEditing = (game) => {
      editingGameId.value = game.id
      editGameName.value = game.name
    }

    const cancelEditing = () => {
      editingGameId.value = null
      editGameName.value = ''
    }

    const updateGame = async (gameId) => {
      if (!isAdmin.value) {
        error.value = 'You do not have permission to update games.'
        return
      }
      try {
        const response = await axios.put(`http://localhost:8000/games/${gameId}`, { name: editGameName.value }, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        console.log('Game updated:', response.data)
        message.value = 'Game updated successfully!'
        editingGameId.value = null
        error.value = null
        await fetchGames()
      } catch (err) {
        console.error('Failed to update game:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to update game. Please try again.'
        message.value = null
      }
    }

    const deleteGame = async (gameId) => {
      if (!isAdmin.value) {
        error.value = 'You do not have permission to delete games.'
        return
      }
      if (confirm('Are you sure you want to delete this game?')) {
        try {
          await axios.delete(`http://localhost:8000/games/${gameId}`, {
            headers: { Authorization: `Bearer ${store.state.token}` }
          })
          message.value = 'Game deleted successfully!'
          error.value = null
          await fetchGames()
        } catch (err) {
          console.error('Failed to delete game:', err)
          error.value = err.response && err.response.data && err.response.data.detail
            ? err.response.data.detail
            : 'Failed to delete game. Please try again.'
          message.value = null
        }
      }
    }

    const isEditing = (gameId) => editingGameId.value === gameId

    onMounted(() => {
      fetchGames()
    })

    return {
      games,
      newGame,
      editGameName,
      editingGameId,
      createGame,
      updateGame,
      deleteGame,
      startEditing,
      cancelEditing,
      isEditing,
      error,
      message,
      isAdmin
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

.btn-danger, .btn-secondary, .btn-success, .btn-warning {
  margin-left: 10px;
}
</style>