<script setup lang="ts">
import { ref } from 'vue';

import Toggle from './Toggle.vue';
import SignupForm from './SignupForm.vue';
import SigninForm from './SigninForm.vue';

export type UserAuth = 'Sign Up' | 'Sign In'

const activeBtn = ref<UserAuth>("Sign Up")
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}
</script>

<template>
    <section
        class="row-start-1 row-span-5 col-start-2 flex flex-col justify-center items-center gap-6 px-4 pt-8 bg-white/10 backdrop-blur-lg rounded-lg shadow-md shadow-sky-800">
        <Toggle :activeBtn="activeBtn" @activateBtn="activateBtn" />
        <Transition name="fade" mode="out-in">
            <KeepAlive>
                <component :is="activeBtn === 'Sign Up' ? SignupForm : SigninForm" />
            </KeepAlive>
        </Transition>
    </section>
</template>

<style scoped>
input {
    @apply w-48
}

.fade-enter-active,
.fade-leave-active {
    @apply transition-all duration-300 ease-out
}

.fade-enter-from,
.fade-leave-to {
    @apply translate-x-4 opacity-0
}
</style>