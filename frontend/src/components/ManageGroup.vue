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
    const newGroup = ref({ name: '', code: '', game_id: null })
    const error = ref(null)
    const message = ref(null)

    const fetchGroups = async () => {
      try {
        const response = await axios.get('http://localhost:8001/groups', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        groups.value = response.data
        error.value = null
      } catch (err) {
        console.error('Failed to fetch groups:', err)
        error.value = 'Failed to fetch groups. Please try again.'
      }
    }

    const fetchGames = async () => {
      try {
        const response = await axios.get('http://localhost:8001/games', {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        games.value = response.data
      } catch (err) {
        console.error('Failed to fetch games:', err)
        error.value = 'Failed to fetch games. Please try again.'
      }
    }

    const createGroup = async () => {
      try {
        console.log('Sending group data:', newGroup.value)
        const response = await axios.post('http://localhost:8001/groups', newGroup.value, {
          headers: {
            'Authorization': `Bearer ${store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        console.log('Group created:', response.data)
        message.value = 'Group created successfully!'
        newGroup.value = { name: '', code: '', game_id: null }
        error.value = null
        await fetchGroups()
      } catch (err) {
        console.error('Failed to create group:', err.response && err.response.data ? err.response.data : err.message)
        error.value = `Failed to create group: ${err.response && err.response.data && err.response.data.detail ? err.response.data.detail : 'Unknown error'}`
        message.value = null
      }
    }

    const deleteGroup = async (groupId) => {
      if (confirm('Are you sure you want to delete this group?')) {
        try {
          await axios.delete(`http://localhost:8001/groups/${groupId}`, {
            headers: { Authorization: `Bearer ${store.state.token}` }
          })
          message.value = 'Group deleted successfully!'
          error.value = null
          await fetchGroups()
        } catch (err) {
          console.error('Failed to delete group:', err)
          error.value = `Failed to delete group: ${err.response && err.response.data && err.response.data.detail ? err.response.data.detail : 'Unknown error'}`
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
      message
    }
  }
}
</script>