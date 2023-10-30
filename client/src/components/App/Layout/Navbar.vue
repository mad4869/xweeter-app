<script setup lang="ts">
import Logo from '@/components/App/Logo.vue';
import useAuthStore from '@/stores/useAuthStore';

const authStore = useAuthStore()

defineEmits<{
    (e: 'show-signout-modal'): void
}>()
</script>

<template>
    <nav
        class="sticky top-0 z-20 grid grid-cols-4 px-20 py-4 mx-auto text-white border-b border-solid place-items-center bg-sky-600/90 backdrop-blur border-sky-900 dark:bg-slate-900/90 dark:text-white dark:shadow-md dark:shadow-sky-600/50">
        <div class="col-span-1"></div>
        <div class="flex items-center justify-center col-span-2">
            <router-link to="/home" title="Home">
                <Logo size="sm" />
            </router-link>
        </div>
        <div v-if="authStore.getIsAuthenticated" class="flex items-center justify-center col-span-1 text-sm">
            <button 
                class="navbar-menu hover:bg-sky-600/10">
                <router-link 
                    :to="`/users/${authStore.getSignedInUserId}`" 
                    title="View your profile" 
                    active-class="active">
                    Profile
                </router-link>
            </button>
            <button  
                class="navbar-menu hover:bg-sky-600/10">
                <router-link 
                    to="/leaderboard" 
                    title="View leaderboard" 
                    active-class="active">
                    Leaderboard
                </router-link>
            </button>
            <button 
                v-if="authStore.getSignedInRole === 'admin'" 
                class="navbar-menu hover:bg-sky-600/10">
                <router-link 
                    to="/admin" 
                    title="View admin dashboard"
                    active-class="active">
                    Admin
                </router-link>
            </button>
            <button 
                class="navbar-menu hover:bg-red-600/80 dark:hover:bg-red-600/30 hover:text-white" 
                @click="$emit('show-signout-modal')"
                title="Sign Out">
                Sign Out
            </button>
        </div>
    </nav>
</template>

<style scoped>
.active {
    @apply text-slate-900 dark:text-sky-600
}
.navbar-menu {
    @apply px-2 py-1 rounded-md cursor-pointer transition-colors ease-in hover:backdrop-blur-md
}
</style>