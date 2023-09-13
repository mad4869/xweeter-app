<script setup lang="ts">
import Logo from '../Logo.vue';

const menus = [
    { path: '/profile', name: 'Profile' },
    { path: '/leaderboard', name: 'Leaderboard' },
    { path: '/logout', name: 'Logout' },
]
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
        <ul class="col-span-1 flex justify-center items-center gap-8">
            <router-link v-for="menu in menus" :key="menu.name" :to="menu.path"
                class="px-2 py-1 rounded-md cursor-pointer transition-colors ease-in hover:bg-sky-600/10 hover:backdrop-blur-md">
                {{ menu.name }}
            </router-link>
        </ul>
    </nav>
</template>