<script setup lang="ts">
import { ref } from 'vue';

import Toggle from '../../components/App/Toggle.vue';
import SignupForm from '../../components/App/SignupForm.vue';
import SigninForm from '../../components/App/SigninForm.vue';
import { UserAuth } from '../../types/auth'

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}
</script>

<template>
    <section
        class="row-start-1 row-span-5 col-start-2 flex flex-col justify-center items-center gap-2 px-32 py-8 bg-white/10 backdrop-blur-lg rounded-lg shadow-lg shadow-sky-800">
        <Toggle :activeBtn="activeBtn" @activateBtn="activateBtn" />
        <Transition name="fade" mode="out-in">
            <KeepAlive>
                <component :is="activeBtn === UserAuth.SignUp ? SignupForm : SigninForm" />
            </KeepAlive>
        </Transition>
    </section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    @apply transition-all duration-300 ease-out
}

.fade-enter-from,
.fade-leave-to {
    @apply translate-x-4 opacity-0
}
</style>