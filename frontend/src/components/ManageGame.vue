<template>
  <div class="manage-game">
    <h2>Manage Games</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="game in games" :key="game.id">
          <td>{{ game.id }}</td>
          <td>{{ game.name }}</td>
          <td>
            <button @click="editGame(game)" class="btn btn-sm btn-primary mr-2">Edit</button>
            <button @click="deleteGame(game.id)" class="btn btn-sm btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <router-link to="/add-game" class="btn btn-success">Add New Game</router-link>

    <!-- Edit Game Modal -->
    <div class="modal" tabindex="-1" v-if="showEditModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Game</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEdit">
              <div class="mb-3">
                <label for="gameName" class="form-label">Game Name</label>
                <input type="text" class="form-control" id="gameName" v-model="editingGame.name" required>
              </div>
              <button type="submit" class="btn btn-primary">Update Game</button>
            </form>
          </div>
        </div>
      </div>
    </div>
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
    const showEditModal = ref(false)
    const editingGame = ref(null)

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8001/games', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        games.value = response.data
      } catch (error) {
        console.error('Failed to fetch games:', error)
      }
    }

    const editGame = (game) => {
      editingGame.value = { ...game }
      showEditModal.value = true
    }

    const submitEdit = async () => {
      try {
        await axios.put(`http://localhost:8001/games/${editingGame.value.id}`, editingGame.value, {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        closeModal()
        await fetchGames()
      } catch (error) {
        console.error('Failed to update game:', error)
        alert('Failed to update game. Please try again.')
      }
    }

    const deleteGame = async (id) => {
      if (confirm('Are you sure you want to delete this game?')) {
        try {
          await axios.delete(`http://localhost:8001/games/${id}`, {
            headers: { Authorization: `Bearer ${store.state.token}` }
          })
          await fetchGames()
        } catch (error) {
          console.error('Failed to delete game:', error)
          alert('Failed to delete game. Please try again.')
        }
      }
    }

    const closeModal = () => {
      showEditModal.value = false
      editingGame.value = null
    }

    onMounted(fetchGames)

    return {
      games,
      showEditModal,
      editingGame,
      editGame,
      submitEdit,
      deleteGame,
      closeModal
    }
  }
}
</script>