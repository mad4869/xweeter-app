<script setup lang="ts">
defineProps<{
    message: string,
    category: 'success' | 'error'
}>()

const categories = {
    success: 'bg-emerald-600',
    error: 'bg-red-600',
}
</script>

<template>
    <div class="fixed left-1/2 bottom-4 -translate-x-1/2 flex items-center gap-4 px-4 py-2 text-white rounded-md" :class="categories[category]">
        <div>
            <font-awesome-icon icon="fa-regular fa-sun" class="text-sm" />
        </div>
        <div class="flex-1">
            <p>{{ message }}</p>
        </div>
    </div>
</template>