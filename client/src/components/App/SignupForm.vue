<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required, email, sameAs, minLength, helpers } from '@vuelidate/validators'
import { AxiosError } from 'axios';

import InputField from './InputField.vue';
import useAuth from '../../composables/useAuth';
import { AuthResponse, AuthResponseWoUser } from '../../types/auth'
import { sendReqWoCookie } from '../../utils/axiosInstances';

defineProps({
    useTitle: {
        type: Boolean,
        default: true
    }
})

const authStore = useAuth()

const userData = reactive({
    username: '',
    fullname: '',
    email: '',
    password: '',
    confirmPassword: ''
})

const password = computed(() => userData.password)

const rules = {
    username: { required },
    fullname: { required },
    email: { required, email },
    password: { required, minLength: minLength(6) },
    confirmPassword: { 
        required, 
        sameAsPassword: helpers.withMessage('This should match the password', sameAs(password)) 
    }
}

const v$ = useVuelidate(rules, userData)

const isError = ref(false)
const errorMsg = ref('')
const isLoading = ref(false)

const signupAndIn = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqWoCookie.post<AuthResponse | undefined>('/api/signup', userData)

        if (data?.success) {
            await authStore.signin({ username: userData.username, password: userData.password })

            isLoading.value = false

            if (authStore.getErrorMsg) {
                isError.value = true
                errorMsg.value = authStore.getErrorMsg

                setInterval(() => {
                    isError.value = false
                    errorMsg.value = ''
                }, 3000)
            }
        }
    } catch (error) {
        const err = error as AxiosError

        if (err.response?.status === 400) {
            isLoading.value = false
            isError.value = true

            const data = err.response.data as AuthResponseWoUser
            errorMsg.value = data.message

            setInterval(() => {
                isError.value = false
                errorMsg.value = ''
            }, 3000)
        }
    }
}
</script>

<template>
    <form 
        class="flex-1 flex flex-col justify-center items-center gap-6 w-full" 
        @submit.prevent="signupAndIn">
        <h3 v-if="useTitle" class="text-2xl text-white font-semibold">Let's get you started!</h3>
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
        <InputField 
            input-id="confirm-password" 
            input-name="confirm-password" 
            input-type="password"
            :input-errors="v$.confirmPassword.$errors" 
            v-model="v$.confirmPassword.$model" 
            label-text="Confirm Password"
            icon="fa-solid fa-lock" />
        <div v-if="isError" class="text-red-400 text-xs">{{ errorMsg }}</div>
        <button 
            type="submit"
            class="uppercase w-24 py-1 bg-sky-600 text-white rounded-md shadow-sm shadow-slate-900/50 transition-colors duration-200 ease-in hover:bg-sky-800 active:shadow-inner disabled:bg-neutral-800 disabled:text-neutral-600 disabled:shadow-none disabled:cursor-not-allowed"
            title="Sign Up"
            :disabled="v$.$invalid">
            <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
            {{ !isLoading ? 'Sign Up' : '' }}
        </button>
    </form>
</template>