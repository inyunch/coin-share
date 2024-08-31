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