<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<template>
    <footer class="flex justify-center items-center py-8 text-slate-400 border-t border-solid border-sky-800">
        <section class="flex flex-col justify-center gap-1 w-3/5">
            <p class="text-xl font-semibold">Zweet</p>
            <p class="text-xs">Copyright {{ year }}</p>
        </section>
    </footer>
</template>