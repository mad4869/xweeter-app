<script setup lang="ts">
import { ref } from 'vue';

const activeBtn = ref("Sign Up")
const activateBtn = (btn: string) => {
    activeBtn.value = btn
}
</script>

<template>
    <div class="flex items-center w-40 border border-solid border-sky-600 rounded-lg overflow-hidden">
        <button :class="{ active: activeBtn === 'Sign Up' }" @click="activateBtn('Sign Up')">
            Sign Up
        </button>
        <button :class="{ active: activeBtn === 'Sign In' }" @click="activateBtn('Sign In')">
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