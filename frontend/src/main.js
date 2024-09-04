import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import config from './config'  // Import the config file

const app = createApp(App)

// Optionally, you can make the config available globally
app.config.globalProperties.$config = config

// If you want to use the api service globally (optional)
import api from './services/api'
app.config.globalProperties.$api = api

app.use(store).use(router).mount('#app')

// Optionally, you can log the API base URL to confirm it's loaded correctly
console.log('API Base URL:', config.apiBaseUrl)