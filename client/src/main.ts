import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faSun, faMoon, faUser, faKeyboard } from '@fortawesome/free-regular-svg-icons'
import './style.css'

import App from './App.vue'
import router from './routes'

library.add(faSun, faMoon, faUser, faKeyboard)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.mount('#app')
