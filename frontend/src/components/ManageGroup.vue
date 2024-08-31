<template>
  <div class="manage-group">
    <h2>Manage Groups</h2>
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Code</th>
          <th>Game</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="group in groups" :key="group.id">
          <td>{{ group.name }}</td>
          <td>{{ group.code }}</td>
          <td>{{ group.game.name }}</td>
        </tr>
      </tbody>
    </table>
    <button class="btn btn-primary" @click="showAddGroupModal = true">Add New Group</button>

    <!-- Add Group Modal -->
    <div class="modal" tabindex="-1" v-if="showAddGroupModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Group</h5>
            <button type="button" class="btn-close" @click="showAddGroupModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addGroup">
              <div class="mb-3">
                <label for="groupName" class="form-label">Group Name</label>
                <input type="text" class="form-control" id="groupName" v-model="newGroup.name" required>
              </div>
              <div class="mb-3">
                <label for="groupCode" class="form-label">Group Code</label>
                <input type="text" class="form-control" id="groupCode" v-model="newGroup.code" required>
              </div>
              <div class="mb-3">
                <label for="gameId" class="form-label">Game</label>
                <select class="form-select" id="gameId" v-model="newGroup.game_id" required>
                  <option v-for="game in games" :key="game.id" :value="game.id">{{ game.name }}</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">Add Group</button>
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
  name: 'ManageGroup',
  setup() {
    const store = useStore()
    const groups = ref([])
    const games = ref([])
    const showAddGroupModal = ref(false)
    const newGroup = ref({ name: '', code: '', game_id: null })

    const fetchGroups = async () => {
      try {
        const response = await axios.get('http://localhost:8001/groups', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        groups.value = response.data
      } catch (error) {
        console.error('Failed to fetch groups:', error)
      }
    }

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

    const addGroup = async () => {
      try {
        await axios.post('http://localhost:8001/groups', newGroup.value, {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        showAddGroupModal.value = false
        newGroup.value = { name: '', code: '', game_id: null }
        await fetchGroups()
      } catch (error) {
        console.error('Failed to add group:', error)
        alert('Failed to add group. Please try again.')
      }
    }

    onMounted(() => {
      fetchGroups()
      fetchGames()
    })

    return { groups, games, showAddGroupModal, newGroup, addGroup }
  }
}
</script>