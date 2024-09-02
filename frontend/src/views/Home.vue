<template>
  <div class="home">
    <h1>Welcome to Coin Share</h1>
    <p>You are logged in as {{ user.name }}</p>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    const user = computed(() => store.getters.currentUser)

    return { user }
  }
}
</script>