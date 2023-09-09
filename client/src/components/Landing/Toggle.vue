<script setup lang="ts">
defineProps<{
    activeBtn: 'Sign Up' | 'Sign In'
}>()
defineEmits<{
    (e: 'activateBtn', btn: 'Sign Up' | 'Sign In'): void
}>()
</script>

<template>
    <div class="flex items-center w-40 border border-solid border-sky-600 rounded-lg overflow-hidden">
        <button :class="{ active: activeBtn === 'Sign Up' }" @click="$emit('activateBtn', 'Sign Up')">
            Sign Up
        </button>
        <button :class="{ active: activeBtn === 'Sign In' }" @click="$emit('activateBtn', 'Sign In')">
            Sign In
        </button>
    </div>
</template>

<style scoped>
button {
    @apply w-1/2 px-2 py-1 text-white
}

.active {
    @apply bg-sky-600 font-medium
}
</style>