import { createRouter, createWebHashHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'

import Home from '../pages/Home.vue'
import Landing from '../pages/Landing.vue'
import Profile from '../pages/Profile.vue'
import Leaderboard from '../pages/Leaderboard.vue'
// import useAuth from '../composables/useAuth'

const routes = [
    { 
        path: '/',  
        component: Landing, 
        beforeEnter: async (_: RouteLocationNormalized, __: RouteLocationNormalized, next: NavigationGuardNext) => {
            next()
        // const authStore = useAuth()
        // await authStore.getUser()

        // if (authStore.getIsAuthenticated) {
        //     next('/home')
        // } else {
        //     next()
        // }
    }},
    { path: '/home', component: Home },
    { path: '/profile', component: Profile },
    { path: '/leaderboard', component: Leaderboard }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router