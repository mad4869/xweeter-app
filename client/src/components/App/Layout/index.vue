<script setup lang="ts">
import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
</script>

<template>
    <Navbar />
    <main class="grid grid-cols-5 gap-x-4 w-full px-4 py-4">
        <aside class="sticky top-20 col-span-1 flex flex-col justify-center gap-4 h-side">
            <slot name="sidebarLeft"></slot>
        </aside>
        <article class="col-span-3 flex flex-col gap-4">
            <slot></slot>
        </article>
        <aside class="sticky top-20 col-span-1 flex flex-col justify-center gap-4 h-side">
            <slot name="sidebarRight"></slot>
        </aside>
    </main>
    <Footer />
</template>

<style scoped>
.h-side {
    height: calc(100vh - 6rem);
}
</style>
