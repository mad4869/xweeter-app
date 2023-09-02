import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faSun, faMoon, faUser } from '@fortawesome/free-regular-svg-icons'
import './style.css'

import App from './App.vue'

library.add(faSun, faMoon, faUser)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
