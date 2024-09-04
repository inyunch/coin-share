<template>
  <div class="container mt-4">
    <h1 class="mb-4">Manage Games</h1>
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Existing Games</h5>
        <button class="btn btn-primary" @click="showModal = true">Create Game</button>
      </div>
      <div class="card-body">
        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        <div v-if="message" class="alert alert-success" role="alert">
          {{ message }}
        </div>
        <table class="table table-striped table-hover">
          <thead class="thead-light">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="game in games" :key="game.id">
              <td>{{ game.id }}</td>
              <td>
                <span v-if="!isEditing(game.id)">{{ game.name }}</span>
                <input v-else v-model="editGameName" type="text" class="form-control form-control-sm" />
              </td>
              <td>
                <button @click="startEditing(game)" class="btn btn-sm btn-outline-info" v-if="isAdmin && !isEditing(game.id)">Edit</button>
                <button @click="updateGame(game.id)" class="btn btn-sm btn-outline-success" v-if="isAdmin && isEditing(game.id)">Save</button>
                <button @click="cancelEditing" class="btn btn-sm btn-outline-secondary" v-if="isAdmin && isEditing(game.id)">Cancel</button>
                <button @click="deleteGame(game.id)" class="btn btn-sm btn-outline-danger" v-if="isAdmin && !isEditing(game.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Game Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-content">
          <h3 class="modal-title">Add New Game</h3>
          <form @submit.prevent="createGame">
            <div class="form-group">
              <label for="gameName">Game Name</label>
              <input v-model="newGame.name" type="text" class="form-control" id="gameName" required>
            </div>
            <div class="modal-actions">
              <button type="submit" class="btn btn-primary">Create Game</button>
              <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { useStore } from 'vuex';

export default {
  name: 'ManageGame',
  setup() {
    const store = useStore();
    const games = ref([]);
    const newGame = ref({ name: '' });
    const editGameName = ref('');
    const editingGameId = ref(null);
    const error = ref(null);
    const message = ref(null);
    const showModal = ref(false);

    const isAdmin = computed(() => store.state.user && store.state.user.role === 'admin');

    const isEditing = (gameId) => editingGameId.value === gameId;

    const fetchGames = async () => {
      try {
        const response = await api.get('/games');
        games.value = response.data;
        error.value = null;
      } catch (err) {
        console.error('Failed to fetch games:', err);
        error.value = (err.response && err.response.data && err.response.data.detail)
          ? err.response.data.detail
          : 'Failed to fetch games. Please try again.';
      }
    };

    const createGame = async () => {
      if (!isAdmin.value) {
        error.value = 'You do not have permission to create games.';
        return;
      }
      try {
        const response = await api.post('/games', newGame.value);
        console.log('Game created:', response.data);
        message.value = 'Game created successfully!';
        newGame.value.name = '';
        error.value = null;
        await fetchGames();
        showModal.value = false;
      } catch (err) {
        console.error('Failed to create game:', err);
        error.value = (err.response && err.response.data && err.response.data.detail)
          ? err.response.data.detail
          : 'Failed to create game. Please try again.';
        message.value = null;
      }
    };

    const startEditing = (game) => {
      editingGameId.value = game.id;
      editGameName.value = game.name;
    };

    const cancelEditing = () => {
      editingGameId.value = null;
      editGameName.value = '';
    };

    const updateGame = async (gameId) => {
      if (!isAdmin.value) {
        error.value = 'You do not have permission to update games.';
        return;
      }
      try {
        const response = await api.put(`/games/${gameId}`, { name: editGameName.value });
        console.log('Game updated:', response.data);
        message.value = 'Game updated successfully!';
        cancelEditing();
        await fetchGames();
      } catch (err) {
        console.error('Failed to update game:', err);
        error.value = (err.response && err.response.data && err.response.data.detail)
          ? err.response.data.detail
          : 'Failed to update game. Please try again.';
        message.value = null;
      }
    };

    const deleteGame = async (gameId) => {
      if (!isAdmin.value) {
        error.value = 'You do not have permission to delete games.';
        return;
      }
      if (confirm('Are you sure you want to delete this game?')) {
        try {
          await api.delete(`/games/${gameId}`);
          message.value = 'Game deleted successfully!';
          error.value = null;
          await fetchGames();
        } catch (err) {
          console.error('Failed to delete game:', err);
          error.value = (err.response && err.response.data && err.response.data.detail)
            ? err.response.data.detail
            : 'Failed to delete game. Please try again.';
          message.value = null;
        }
      }
    };

    onMounted(() => {
      fetchGames();
    });

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
      error,
      message,
      isAdmin,
      isEditing,
      showModal
    };
  }
};
</script>

<style scoped>
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn {
  margin-right: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content {
  padding: 20px;
}

.modal-title {
  margin-bottom: 20px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.modal-actions button {
  margin-left: 10px;
}

.table {
  margin-bottom: 0;
}

.table th {
  border-top: none;
}
</style>