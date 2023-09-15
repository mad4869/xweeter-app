import { createRouter, createWebHashHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'

import Home from '../pages/Home.vue'
import Landing from '../pages/Landing.vue'
import Profile from '../pages/Profile.vue'
import Leaderboard from '../pages/Leaderboard.vue'
import useAuth from '../composables/useAuth';

const routes = [
    { path: '/',  component: Landing},
    { 
        path: '/home',  
        component: Home, 
        meta: {requiresAuth: true}, 
        beforeEnter: (_: RouteLocationNormalized, __: RouteLocationNormalized, next: NavigationGuardNext) => {
            const authStore = useAuth()
            if (authStore.getIsAuthenticated) {
                next()
            } else {
                next('/')
            }
        }
    },
    { path: '/profile', component: Profile },
    { path: '/leaderboard', component: Leaderboard }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router