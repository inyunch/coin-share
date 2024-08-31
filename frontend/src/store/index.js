import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoggedIn: false,
    token: null
  },
  mutations: {
    setLoggedIn(state, value) {
      state.isLoggedIn = value
    },
    setToken(state, token) {
      state.token = token
    }
  },
  actions: {
    login({ commit }, token) {
      commit('setLoggedIn', true)
      commit('setToken', token)
    },
    logout({ commit }) {
      commit('setLoggedIn', false)
      commit('setToken', null)
    }
  },
  modules: {
  }
})