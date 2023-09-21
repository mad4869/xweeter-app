<script setup lang="ts">
import { ref } from 'vue';

import Logo from '../Logo.vue';
import router from '../../../routes';
import useAuth from '../../../composables/useAuth';

const authStore = useAuth()

const isError = ref(false)
const isLoading = ref(false)

const signout = async () => {
    await authStore.signout()

    if (!authStore.getIsAuthenticated) {
        router.push('/')
    } else {
        isError.value = true
        setInterval(() => {
            isError.value = false
        }, 3000)
    }
}
</script>

<template>
    <nav
        class="sticky top-0 grid grid-cols-4 place-items-center mx-auto px-20 py-4 bg-slate-200/90 backdrop-blur text-sky-800 border-b border-solid border-sky-600 z-10 dark:bg-slate-900/90 dark:text-white dark:shadow-md dark:shadow-sky-600/50">
        <div class="col-span-1"></div>
        <div class="col-span-2 flex justify-center items-center">
            <router-link to="/home">
                <Logo size="sm" />
            </router-link>
        </div>
        <div class="col-span-1 flex justify-center items-center gap-4">
            <span v-if="authStore.getIsAuthenticated" class="navbar-menu hover:bg-sky-600/10">
                <router-link to="/profile" title="View your profile">Profile</router-link>
            </span>
            <span v-if="authStore.getIsAuthenticated" class="navbar-menu hover:bg-sky-600/10">
                <router-link to="/leaderboard" title="View leaderboard">Leaderboard</router-link>
            </span>
            <button 
                v-if="authStore.getIsAuthenticated" 
                class="navbar-menu hover:bg-red-600/80 dark:hover:bg-red-600/30 hover:text-white" 
                @click="signout"
                title="Sign Out">
                <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
                {{ !isLoading ? 'Sign Out' : '' }}
            </button>
        </div>
        <div v-if="isError" class="absolute">
            Error occured during sign out process. Please try again
        </div>
    </nav>
</template>

<style scoped>
.navbar-menu {
    @apply px-2 py-1 rounded-md cursor-pointer transition-colors ease-in hover:backdrop-blur-md
}
</style>../../../pages/routes