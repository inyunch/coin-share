<template>
  <div class="manage-group">
    <h2>Manage Groups</h2>
    <form @submit.prevent="createGroup" class="mb-4" v-if="isAdmin || isGroupAdmin">
      <div class="form-group">
        <label for="groupName">Group Name</label>
        <input v-model="newGroup.name" type="text" class="form-control" id="groupName" required>
      </div>
      <div class="form-group">
        <label for="groupCode">Group Code</label>
        <input v-model="newGroup.code" type="text" class="form-control" id="groupCode" required>
      </div>
      <div class="form-group">
        <label for="gameId">Game</label>
        <select v-model="newGroup.game_id" class="form-control" id="gameId" required>
          <option v-for="game in games" :key="game.id" :value="game.id">{{ game.name }}</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary mt-2">Create Group</button>
    </form>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div v-if="message" class="alert alert-success" role="alert">
      {{ message }}
    </div>
    <h3>Existing Groups</h3>
    <ul class="list-group">
      <li v-for="group in groups" :key="group.id" class="list-group-item d-flex justify-content-between align-items-center">
        {{ group.name }} (Code: {{ group.code }})
        <button @click="deleteGroup(group.id)" class="btn btn-danger btn-sm" v-if="isAdmin || isGroupAdmin">Delete</button>
      </li>
    </ul>
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
    const newGroup = ref({ name: '', code: '', game_id: null })
    const error = ref(null)
    const message = ref(null)

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
        const response = await axios.post('http://localhost:8000/groups', newGroup.value, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        message.value = 'Group created successfully!'
        newGroup.value = { name: '', code: '', game_id: null }
        error.value = null
        await fetchGroups()
      } catch (err) {
        console.error('Failed to create group:', err)
        error.value = err.response && err.response.data && err.response.data.detail
          ? err.response.data.detail
          : 'Failed to create group. Please try again.'
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

    onMounted(() => {
      fetchGroups()
      fetchGames()
    })

    return {
      groups,
      games,
      newGroup,
      createGroup,
      deleteGroup,
      error,
      message,
      isAdmin,
      isGroupAdmin
    }
  }
}
</script>

<style scoped>
.manage-group {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1rem;
}

.list-group-item {
  margin-bottom: 0.5rem;
}

.btn-danger {
  margin-left: 10px;
}
</style>