import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

// Make BootstrapVue available throughout your project
import BootstrapVue3 from 'bootstrap-vue-3'

const app = createApp(App)

// Use BootstrapVue3 in your app
app.use(BootstrapVue3)
app.use(store)
app.use(router)

app.mount('#app')