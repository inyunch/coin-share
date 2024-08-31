<template>
  <div class="add-game">
    <h2>Add New Game</h2>
    <form @submit.prevent="submitGame">
      <div class="mb-3">
        <label for="gameName" class="form-label">Game Name</label>
        <input type="text" class="form-control" id="gameName" v-model="newGame.name" required>
      </div>
      <button type="submit" class="btn btn-primary">Add Game</button>
      <button type="button" class="btn btn-secondary ms-2" @click="cancel">Cancel</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

export default {
  name: 'AddGame',
  setup() {
    const router = useRouter()
    const store = useStore()
    const newGame = ref({ name: '' })

    const submitGame = async () => {
      try {
        await axios.post('http://localhost:8001/games', newGame.value, {
          headers: { Authorization: `Bearer ${store.state.token}` }
        })
        router.push('/manage-game')
      } catch (error) {
        console.error('Failed to add game:', error)
        alert('Failed to add game. Please try again.')
      }
    }

    const cancel = () => {
      router.push('/manage-game')
    }

    return { newGame, submitGame, cancel }
  }
}
</script>