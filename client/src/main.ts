import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faSun, faMoon, faUser as faUserReg } from '@fortawesome/free-regular-svg-icons'
import { faGear, faFont, faUser as faUserSol, faEnvelope, faLock } from '@fortawesome/free-solid-svg-icons'
import './style.css'

import App from './App.vue'
import router from './routes'

library.add(faSun, faMoon, faUserReg, faUserSol, faGear, faFont, faEnvelope, faLock)

const pinia = createPinia()

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(pinia)
app.use(router)
app.mount('#app')
