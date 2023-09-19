<script setup lang="ts">

</script>

<template>
    <footer class="row-start-6 col-span-2 flex justify-end items-center">
        <button
            class="flex items-center gap-2 w-fit px-2 py-1 text-xs text-sky-900 border border-solid border-sky-900 rounded-md transition-transform duration-300 ease-in-out hover:text-sky-600 hover:border-sky-600 group hover:scale-110"
            title="Try the app now!">
            <router-link to="/home">Home</router-link>
            <font-awesome-icon icon="fa-solid fa-arrow-right" class="hidden group-hover:block" />
        </button>
    </footer>
</template>