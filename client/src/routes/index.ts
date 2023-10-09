import { createRouter, createWebHashHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'

import Home from '@/pages/Home.vue'
import Landing from '@/pages/Landing.vue'
import Profile from '@/pages/Profile.vue'
import Leaderboard from '@/pages/Leaderboard.vue'
import Trending from '@/pages/Trending.vue'
import Xweet from '@/pages/Xweet.vue'
import Admin from '@/pages/Admin.vue'
import useAuthStore from '@/stores/useAuthStore'

const routes = [
    { 
        path: '/',  
        component: Landing, 
        beforeEnter: async (_: RouteLocationNormalized, __: RouteLocationNormalized, next: NavigationGuardNext) => {
        const authStore = useAuthStore()
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
    { path: '/trending', component: Trending },
    { path: '/xweets/:id', component: Xweet },
    { path: '/admin', component: Admin }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router