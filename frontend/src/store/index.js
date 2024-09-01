import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null,
  },
  getters: {
    isLoggedIn: state => !!state.token,
    currentUser: state => state.user,
  },
  mutations: {
    auth_success(state, { token, user }) {
      state.token = token
      state.user = user
    },
    logout(state) {
      state.token = ''
      state.user = null
    },
  },
  actions: {
    async login({ commit }, user) {
      try {
        const params = new URLSearchParams()
        params.append('username', user.username)
        params.append('password', user.password)

        const res = await axios.post('http://localhost:8000/token', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        const token = res.data.access_token
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

        // Fetch user details
        const userDetails = await axios.get('http://localhost:8000/users/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        localStorage.setItem('user', JSON.stringify(userDetails.data))

        commit('auth_success', { token, user: userDetails.data })
        return true
      } catch (err) {
        console.error('Login error:', err.response ? err.response.data : err)
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        return false
      }
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },
    async register({ dispatch }, user) {
      try {
        await axios.post('http://localhost:8000/users', user)
        return dispatch('login', user)
      } catch (err) {
        console.error('Registration error:', err.response ? err.response.data : err)
        throw err
      }
    },
    async fetchUserProfile({ commit }) {
      try {
        const res = await axios.get('http://localhost:8000/users/me')
        commit('auth_success', { token: this.state.token, user: res.data })
      } catch (err) {
        console.error('Error fetching user profile:', err.response ? err.response.data : err)
        commit('logout')
      }
    },
  },
  modules: {
  }
})