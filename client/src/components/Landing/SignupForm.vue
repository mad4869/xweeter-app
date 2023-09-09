<script setup lang="ts">
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'

const state = reactive({
    username: '',
    full_name: '',
    email: '',
    password: ''
})
const rules = {
    username: { required },
    full_name: { required },
    email: { required, email },
    password: { required }
}

const v$ = useVuelidate(rules, state)
</script>

<template>
    <form class="flex-1 flex flex-col justify-center items-center gap-2 w-full">
        <div :class="{ error: v$.full_name.$errors.length }">
            <input type="text" v-model="v$.full_name.$model">
            <div class="" v-for="error of v$.full_name.$errors" :key="error.$uid">
                <div class="text-red-800">{{ error.$message }}</div>
            </div>
        </div>
        <div :class="{ error: v$.username.$errors.length }">
            <input type="text" v-model="v$.username.$model">
            <div class="" v-for="error of v$.username.$errors" :key="error.$uid">
                <div class="text-red-800">{{ error.$message }}</div>
            </div>
        </div>
        <div :class="{ error: v$.email.$errors.length }">
            <input type="email" v-model="v$.email.$model">
            <div class="" v-for="error of v$.email.$errors" :key="error.$uid">
                <div class="text-red-800">{{ error.$message }}</div>
            </div>
        </div>
        <div :class="{ error: v$.password.$errors.length }">
            <input type="password" v-model="v$.password.$model">
            <div class="" v-for="error of v$.password.$errors" :key="error.$uid">
                <div class="text-red-800">{{ error.$message }}</div>
            </div>
        </div>
    </form>
</template>

<style scoped></style>