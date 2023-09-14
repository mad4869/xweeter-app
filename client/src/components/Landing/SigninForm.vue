<script setup lang="ts">
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'

import InputField from './InputField.vue';
import useAuth from '../../composables/auth'
import router from '../../routes';

const credentials = reactive({
    username: '',
    password: ''
})
const rules = {
    username: { required },
    password: { required }
}

const v$ = useVuelidate(rules, credentials)

const authStore = useAuth()

const submitForm = async () => {
    try {
        await authStore.signin(credentials)

        if (authStore.getIsAuthenticated) {
            router.push('/home')
        }
    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
    <form class="flex-1 flex flex-col items-center gap-6 w-full" @submit.prevent="submitForm">
        <h3 class="text-2xl text-white font-semibold">Welcome back!</h3>
        <InputField input-id="username" input-name="username" input-type="text" :input-errors="v$.username.$errors"
            v-model="v$.username.$model" label-text="Username" icon="fa-solid fa-user" />
        <InputField input-id="password" input-name="password" input-type="password" :input-errors="v$.password.$errors"
            v-model="v$.password.$model" label-text="Password" icon="fa-solid fa-lock" />
        <button type="submit"
            class="uppercase px-4 py-1 bg-sky-600 text-white rounded-md shadow-sm shadow-slate-900/50 hover:bg-sky-800 active:shadow-inner">
            Sign In
        </button>
    </form>
</template>