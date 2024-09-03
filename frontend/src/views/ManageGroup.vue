<template>
  <div class="container mt-4">
    <h1 class="mb-4">Manage Groups</h1>
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Existing Groups</h5>
        <button class="btn btn-primary" @click="showModal = true" v-if="isAdmin || isGroupAdmin">Create Group</button>
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
              <th>Name</th>
              <th>Code</th>
              <th>Game</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="group in groups" :key="group.id">
              <td>
                <span v-if="!isEditing(group.id)">{{ group.name || 'Unknown' }}</span>
                <input v-else v-model="editGroupName" type="text" class="form-control form-control-sm" />
              </td>
              <td>{{ group.code || 'N/A' }}</td>
              <td>{{ getGameName(group.game_id) }}</td>
              <td>
                <template v-if="!isEditing(group.id)">
                  <button @click="startEditing(group)" class="btn btn-sm btn-outline-info" v-if="isAdmin || isGroupAdmin">Edit</button>
                  <button @click="deleteGroup(group.id)" class="btn btn-sm btn-outline-danger" v-if="isAdmin || isGroupAdmin">Delete</button>
                </template>
                <template v-else>
                  <button @click="updateGroup(group.id)" class="btn btn-sm btn-outline-success">Save</button>
                  <button @click="cancelEditing" class="btn btn-sm btn-outline-secondary">Cancel</button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Group Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-content">
          <h3 class="modal-title">Add New Group</h3>
          <form @submit.prevent="createGroup">
            <div class="form-group">
              <label for="groupNameInput">Group Name</label>
              <input v-model="newGroup.name" type="text" class="form-control" id="groupNameInput" required>
            </div>
            <div class="form-group">
              <label for="gameIdSelect">Game</label>
              <select v-model="newGroup.game_id" class="form-control" id="gameIdSelect" required>
                <option v-for="game in games" :key="game.id" :value="game.id">{{ game.name }}</option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="submit" class="btn btn-primary">Create Group</button>
              <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'

export default {
  name: 'ManageGroup',
  setup() {
    const store = useStore()
    const groups = ref([])
    const games = ref([])
    const newGroup = ref({ name: '', game_id: null })
    const editGroupName = ref('')
    const editGroupGameId = ref(null)
    const editingGroupId = ref(null)
    const error = ref(null)
    const message = ref(null)
    const showModal = ref(false)

    const isAdmin = computed(() => store.state.user && store.state.user.role === 'admin')
    const isGroupAdmin = computed(() => store.state.user && store.state.user.role === 'group_admin')

    const fetchGroups = async () => {
      try {
        const response = await axios.get('http://localhost:8000/groups', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        groups.value = response.data
        error.value = null
      } catch (err) {
        console.error('Failed to fetch groups:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to fetch groups. Please try again.'
      }
    }

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8000/games', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        games.value = response.data
      } catch (err) {
        console.error('Failed to fetch games:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to fetch games. Please try again.'
      }
    }

    const createGroup = async () => {
      if (!isAdmin.value && !isGroupAdmin.value) {
        error.value = 'You do not have permission to create groups.'
        return
      }
      try {
        await axios.post('http://localhost:8000/groups', newGroup.value, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        message.value = 'Group created successfully!'
        newGroup.value = { name: '', game_id: null }
        error.value = null
        showModal.value = false
        await fetchGroups()
      } catch (err) {
        console.error('Failed to create group:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to create group. Please try again.'
        message.value = null
      }
    }

    const startEditing = (group) => {
      editingGroupId.value = group.id
      editGroupName.value = group.name
      editGroupGameId.value = group.game_id
    }

    const cancelEditing = () => {
      editingGroupId.value = null
      editGroupName.value = ''
      editGroupGameId.value = null
    }

    const updateGroup = async (groupId) => {
      if (!isAdmin.value && !isGroupAdmin.value) {
        error.value = 'You do not have permission to update groups.'
        return
      }
      try {
        await axios.put(`http://localhost:8000/groups/${groupId}`, {
          name: editGroupName.value,
          game_id: editGroupGameId.value
        }, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        message.value = 'Group updated successfully!'
        cancelEditing()
        await fetchGroups()
      } catch (err) {
        console.error('Failed to update group:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to update group. Please try again.'
        message.value = null
      }
    }

    const deleteGroup = async (groupId) => {
      if (!isAdmin.value && !isGroupAdmin.value) {
        error.value = 'You do not have permission to delete groups.'
        return
      }
      if (confirm('Are you sure you want to delete this group?')) {
        try {
          await axios.delete(`http://localhost:8000/groups/${groupId}`, {
            headers: { Authorization: `Bearer ${store.state.token}` }
          })
          message.value = 'Group deleted successfully!'
          error.value = null
          await fetchGroups()
        } catch (err) {
          console.error('Failed to delete group:', err)
          error.value = err.response && err.response.data && err.response.data.detail
            ? err.response.data.detail
            : 'Failed to delete group. Please try again.'
          message.value = null
        }
      }
    }

    const getGameName = (gameId) => {
      const game = games.value.find(g => g.id === gameId)
      return game ? game.name : 'Unknown'
    }

    const isEditing = (groupId) => editingGroupId.value === groupId

    onMounted(() => {
      fetchGroups()
      fetchGames()
    })

    return {
      groups,
      games,
      newGroup,
      editGroupName,
      editGroupGameId,
      editingGroupId,
      createGroup,
      updateGroup,
      deleteGroup,
      startEditing,
      cancelEditing,
      getGameName,
      isEditing,
      error,
      message,
      isAdmin,
      isGroupAdmin,
      showModal
    }
  }
}
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