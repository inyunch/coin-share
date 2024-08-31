<template>
  <div class="manage-group">
    <h2>Manage Groups</h2>
    <form @submit.prevent="createGroup">
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
      <button type="submit" class="btn btn-primary">Create Group</button>
    </form>
    <h3>Existing Groups</h3>
    <ul class="list-group">
      <li v-for="group in groups" :key="group.id" class="list-group-item">
        {{ group.name }} (Code: {{ group.code }})
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ManageGroup',
  setup() {
    const groups = ref([])
    const games = ref([])
    const newGroup = ref({ name: '', code: '', game_id: null })

    const fetchGroups = async () => {
      try {
        const response = await axios.get('http://localhost:8001/groups')
        groups.value = response.data
      } catch (error) {
        console.error('Failed to fetch groups:', error)
      }
    }

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8001/games')
        games.value = response.data
      } catch (error) {
        console.error('Failed to fetch games:', error)
      }
    }

    const createGroup = async () => {
      try {
        await axios.post('http://localhost:8001/groups', newGroup.value)
        newGroup.value = { name: '', code: '', game_id: null }
        await fetchGroups()
      } catch (error) {
        console.error('Failed to create group:', error)
        alert('Failed to create group. Please try again.')
      }
    }

    onMounted(() => {
      fetchGroups()
      fetchGames()
    })

    return { groups, games, newGroup, createGroup }
  }
}
</script>