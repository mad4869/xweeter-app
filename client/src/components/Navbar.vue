<script setup lang="ts">
import Logo from './Logo.vue';
</script>

<template>
    <nav
        class="grid grid-cols-4 place-items-center mx-auto px-20 py-4 text-white border-b border-solid border-sky-600 shadow-md shadow-sky-600/50">
        <div class="col-span-1"></div>
        <div class="col-span-2 flex justify-center items-center">
            <Logo size="w-8" />
        </div>
        <ul class="col-span-1 flex justify-center items-center gap-4">
            <li>Profile</li>
            <li>Leaderboard</li>
            <li>Logout</li>
        </ul>
    </nav>
</template>

<style scoped></style>