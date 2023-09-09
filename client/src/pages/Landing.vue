<script setup lang="ts">
import Hero from '../components/Landing/Hero.vue'
import Cta from '../components/Landing/Cta.vue';
</script>

<template>
    <main
        class="grid grid-cols-2 gap-x-4 w-[100vw] h-[100vh] px-20 py-20 bg-gradient-to-tl from-slate-900 from-20% to-sky-800">
        <Hero />
        <Cta />
    </main>
</template>