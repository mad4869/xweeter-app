<script setup lang="ts">
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'
import axios from 'axios'

import InputField from './InputField.vue';
import router from '../../routes';
import useAuth, { type User } from '../../composables/useAuth';

const authStore = useAuth()

type Response = {
    user: User,
    message: string,
    success: boolean
}

const userData = reactive({
    username: '',
    fullname: '',
    email: '',
    password: ''
})
const rules = {
    username: { required },
    fullname: { required },
    email: { required, email },
    password: { required }
}

const v$ = useVuelidate(rules, userData)

const signupAndIn = async () => {
    try {
        const { data } = await axios.post<Response | undefined>('/api/signup', userData)
        if (data?.success) {
            await authStore.signin({ username: userData.username, password: userData.password })

            if (authStore.getIsAuthenticated) {
                router.push('/home')
            }
        }
    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
    <form class="flex-1 flex flex-col items-center gap-6 w-full" @submit.prevent="signupAndIn">
        <h3 class="text-2xl text-white font-semibold">Let's get you started!</h3>
        <InputField 
            input-id="fullname" 
            input-name="fullname" 
            input-type="text" 
            :input-errors="v$.fullname.$errors"
            v-model="v$.fullname.$model" 
            label-text="Full Name" 
            icon="fa-solid fa-font" />
        <InputField 
            input-id="username" 
            input-name="username" 
            input-type="text" 
            :input-errors="v$.username.$errors"
            v-model="v$.username.$model" 
            label-text="Username" 
            icon="fa-solid fa-user" />
        <InputField 
            input-id="email" 
            input-name="email" 
            input-type="text" 
            :input-errors="v$.email.$errors"
            v-model="v$.email.$model" 
            label-text="Email Address" 
            icon="fa-solid fa-envelope" />
        <InputField 
            input-id="password" 
            input-name="password" 
            input-type="password" 
            :input-errors="v$.password.$errors"
            v-model="v$.password.$model" 
            label-text="Password" 
            icon="fa-solid fa-lock" />
        <button 
            type="submit"
            class="uppercase px-4 py-1 bg-sky-600 text-white rounded-md shadow-sm shadow-slate-900/50 hover:bg-sky-800 active:shadow-inner">
            Sign Up
        </button>
    </form>
</template>