import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    token: localStorage.getItem('token') || null,
    user: null
  },
  mutations: {
    setToken(state, token) {
      state.token = token
    },
    setUser(state, user) {
      state.user = user
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('http://localhost:8001/token', new URLSearchParams({
          username: credentials.username,
          password: credentials.password
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        const token = response.data.access_token
        localStorage.setItem('token', token)
        commit('setToken', token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        return true
      } catch (error) {
        console.error('Login failed:', error.response ? error.response.data : error.message)
        return false
      }
    },
    // ... other actions ...
  },
  getters: {
    isLoggedIn: state => !!state.token
  }
})