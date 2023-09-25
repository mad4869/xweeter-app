<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'

import InputField from './InputField.vue';
import useAuth from '../../composables/useAuth';

defineProps({
    useTitle: {
        type: Boolean,
        default: true
    }
})

const authStore = useAuth()

const credentials = reactive({
    username: '',
    password: ''
})
const rules = {
    username: { required },
    password: { required, minLength: minLength(6) }
}

const v$ = useVuelidate(rules, credentials)

const isError = ref(false)
const isLoading = ref(false)

const signin = async () => {
    isLoading.value = true
    
    await authStore.signin(credentials)
    
    isLoading.value = false

    if (!authStore.getIsAuthenticated) {
        isError.value = true
        setInterval(() => {
            isError.value = false
        }, 3000)
    }
}
</script>

<template>
    <form 
        class="flex-1 relative flex flex-col justify-center items-center gap-6 w-full" 
        @submit.prevent="signin">
        <h3 v-if="useTitle" class="text-2xl text-white font-semibold">Welcome back!</h3>
        <InputField 
            input-id="username" 
            input-name="username" 
            input-type="text" 
            :input-errors="v$.username.$errors"
            v-model="v$.username.$model" 
            label-text="Username" 
            icon="fa-solid fa-user" />
        <InputField 
            input-id="password" 
            input-name="password" 
            input-type="password" 
            :input-errors="v$.password.$errors"
            v-model="v$.password.$model" 
            label-text="Password" 
            icon="fa-solid fa-lock" />
        <div v-if="isError" class="text-red-400 text-xs">{{ authStore.getErrorMsg }}</div>
        <button 
            type="submit"
            class="uppercase w-24 py-1 bg-sky-600 text-white rounded-md shadow-sm shadow-slate-900/50 transition-colors duration-200 ease-in hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:shadow-none disabled:cursor-not-allowed"
            title="Sign In"
            :disabled="v$.$invalid">
            <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
            {{ !isLoading ? 'Sign In' : '' }}
        </button>
    </form>
</template>