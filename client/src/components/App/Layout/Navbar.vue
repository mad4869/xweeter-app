<script setup lang="ts">
import Logo from '../Logo.vue';
import router from '../../../routes';
import useAuth from '../../../composables/useAuth';

const authStore = useAuth()
await authStore.getUser()

const signout = async () => {
    try {
        await authStore.signout()

        if (!authStore.getIsAuthenticated) {
            router.push('/')
        }
    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
    <nav
        class="sticky top-0 grid grid-cols-4 place-items-center mx-auto px-20 py-4 bg-slate-900/90 backdrop-blur text-white border-b border-solid border-sky-600 shadow-md shadow-sky-600/50 z-10">
        <div class="col-span-1"></div>
        <div class="col-span-2 flex justify-center items-center">
            <router-link to="/home">
                <Logo size="sm" />
            </router-link>
        </div>
        <div class="col-span-1 flex justify-center items-center gap-8">
            <span v-if="authStore.getIsAuthenticated" class="navbar-menu hover:bg-sky-600/10">
                <router-link to="/profile">Profile</router-link>
            </span>
            <span v-if="authStore.getIsAuthenticated" class="navbar-menu hover:bg-sky-600/10">
                <router-link to="/leaderboard">Leaderboard</router-link>
            </span>
            <button v-if="authStore.getIsAuthenticated" class="navbar-menu hover:bg-red-600/30" @click="signout">
                Logout
            </button>
        </div>
    </nav>
</template>

<style scoped>
.navbar-menu {
    @apply px-2 py-1 rounded-md cursor-pointer transition-colors ease-in hover:backdrop-blur-md
}
</style>