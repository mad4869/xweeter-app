<script setup lang="ts">

</script>

<template>
    <section class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Settings</span>
        </div>
        <div class="flex items-center gap-2 px-4 group">
            <font-awesome-icon icon="fa-regular fa-sun" class="text-white" />
            <label for="dark-mode"
                class="flex items-center w-9 h-6 px-1 border-2 border-solid border-sky-800 rounded-full group-hover:cursor-pointer peer">
                <input type="checkbox" name="dark-mode" id="dark-mode" role="switch"
                    class="appearance-none w-3 h-3 bg-slate-600 rounded-full transition-all duration-300 checked:translate-x-full checked:bg-sky-600">
            </label>
            <font-awesome-icon icon="fa-regular fa-moon" class="text-white" />
        </div>
    </section>
</template>

<style scoped></style>