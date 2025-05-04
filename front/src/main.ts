import {createApp} from 'vue'
import App from './App.vue'
import {router} from './router'
import api from './api/axios'
import './assets/main.scss'

const app = createApp(App)


app.config.globalProperties.$api = api // доступ до axios як this.$api

app.use(router)
app.mount('#app')
