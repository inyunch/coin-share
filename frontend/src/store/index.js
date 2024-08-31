import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isLoggedIn: false,
    token: null,
    user: null
  },
  mutations: {
    setLoggedIn(state, value) {
      state.isLoggedIn = value
    },
    setToken(state, token) {
      state.token = token
    },
    setUser(state, user) {
      state.user = user
    }
  },
  actions: {
    login({ commit }, token) {
      commit('setLoggedIn', true)
      commit('setToken', token)
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    logout({ commit }) {
      commit('setLoggedIn', false)
      commit('setToken', null)
      commit('setUser', null)
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },
    initializeAuth({ commit, dispatch }) {
      const token = localStorage.getItem('token')
      if (token) {
        commit('setLoggedIn', true)
        commit('setToken', token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        dispatch('fetchUser')
      }
    },
    async fetchUser({ commit }) {
      try {
        const response = await axios.get('http://localhost:8001/users/me')
        commit('setUser', response.data)
      } catch (error) {
        console.error('Failed to fetch user:', error)
        // If fetching user fails, log out
        this.dispatch('logout')
      }
    }
  },
  getters: {
    isLoggedIn: state => state.isLoggedIn,
    user: state => state.user
  }
})