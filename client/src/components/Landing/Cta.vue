<script setup lang="ts">
import { ref } from 'vue';

import Toggle from './Toggle.vue';
import SignupForm from './SignupForm.vue';
import SigninForm from './SigninForm.vue';

const activeBtn = ref<'Sign Up' | 'Sign In'>("Sign Up")
const activateBtn = (btn: "Sign Up" | "Sign In") => {
    activeBtn.value = btn
}
</script>

<template>
    <section
        class="col-start-2 flex flex-col justify-center items-center gap-6 px-4 pt-8 bg-white/10 backdrop-blur-lg rounded-lg shadow-md shadow-sky-800">
        <Toggle :activeBtn="activeBtn" @activateBtn="activateBtn" />
        <component :is="activeBtn === 'Sign Up' ? SignupForm : SigninForm" />
    </section>
</template>

<style scoped>
input {
    @apply w-48
}
</style>