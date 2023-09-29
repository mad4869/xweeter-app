import { createRouter, createWebHashHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'

import Home from '../pages/Home.vue'
import Landing from '../pages/Landing.vue'
import Profile from '../pages/Profile.vue'
import Leaderboard from '../pages/Leaderboard.vue'
import Trending from '../pages/Trending.vue'
import useAuth from '../composables/useAuth'

const routes = [
    { 
        path: '/',  
        component: Landing, 
        beforeEnter: async (_: RouteLocationNormalized, __: RouteLocationNormalized, next: NavigationGuardNext) => {
        const authStore = useAuth()
        await authStore.getUser()

        if (authStore.getIsAuthenticated) {
            next('/home')
        } else {
            next()
        }
    }},
    { path: '/home', component: Home },
    { path: '/users/:id', component: Profile },
    { path: '/leaderboard', component: Leaderboard },
    { path: '/trending', component: Trending }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router