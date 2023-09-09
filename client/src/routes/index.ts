import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '../pages/Home.vue'
import Landing from '../pages/Landing.vue'
import Profile from '../pages/Profile.vue'
import Leaderboard from '../pages/Leaderboard.vue'

const routes = [
    { path: '/',  component: Landing},
    { path: '/home',  component: Home},
    { path: '/profile', component: Profile },
    { path: '/leaderboard', component: Leaderboard }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router