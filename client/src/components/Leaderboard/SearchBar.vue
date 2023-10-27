<script setup lang="ts">
defineProps<{
    keywords: string
}>()
defineEmits<{
    (e: 'update:keywords', value: string): void
}>()
</script>

<template>
    <section class="flex items-center pl-2 overflow-hidden text-white border border-solid rounded-md border-sky-800 max-w-fit focus-within:ring-1 focus-within:ring-sky-600 ml-4">
        <input 
            id="search-bar"
            name="search-bar"
            type="text"
            :value="keywords" 
            @input="$emit('update:keywords', ($event.target as HTMLInputElement).value)"
            class="bg-transparent focus:outline-none" />
        <div class="px-2 py-1 rounded-sm bg-sky-600">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
        </div>
    </section>
</template>