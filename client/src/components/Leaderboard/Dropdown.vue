<script setup lang="ts">
defineProps<{
    entries: number
}>()
defineEmits<{
    (e: 'update:entries', value: number): void
}>()
</script>

<template>
    <section class="flex items-center gap-1 dark:text-white px-4">
        <span>Show</span>
        <select 
            name="leaderboard" 
            id="leaderboard" 
            :value="entries" 
            @change="$emit('update:entries', parseInt(($event.target as HTMLSelectElement).value))"
            class="bg-sky-800 px-2 rounded-md">
            <option :value="5">5</option>
            <option :value="10">10</option>
            <option :value="15">15</option>
            <option :value="20">20</option>
        </select>
        <span>entries</span>
    </section>
</template>