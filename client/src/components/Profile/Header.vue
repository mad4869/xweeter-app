<script setup lang="ts">
import useAuth from '../../composables/useAuth';

const authStore = useAuth()
</script>

<template>
    <section class="relative grid grid-rows-5 h-[50vh] rounded-lg overflow-hidden">
        <div class="row-span-3">
            <img :src="authStore.getSignedInHeader" alt="Header" loading="lazy" class="w-full h-full object-cover">
        </div>
        <div class="absolute flex justify-between items-center w-full bottom-[14vh] px-12">
            <img :src="authStore.getSignedInPfp" alt="Header" loading="lazy"
                class="w-20 h-20 border border-solid border-sky-600 rounded-full shadow-md">
            <button
                class="bg-sky-600 px-4 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-md">Follow</button>
        </div>
        <div class="row-start-4 row-span-2 flex flex-col gap-4 pt-12 px-12 bg-white/10 leading-4">
            <div>
                <p class="text-sky-600 font-bold">{{ authStore.getSignedInFullname }}</p>
                <p class="text-sky-800 text-sm">@{{ authStore.getSignedInUsername }}</p>
            </div>
            <p class="text-xs text-white">{{ authStore.getSignedInBio }}</p>
        </div>
    </section>
</template>