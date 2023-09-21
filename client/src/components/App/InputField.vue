<script setup lang="ts">
import { ErrorObject } from '@vuelidate/core';

defineProps<{
    inputId: string,
    inputName: string,
    inputType: string,
    inputErrors: ErrorObject[],
    modelValue: string,
    labelText: string,
    icon: string
}>()
</script>

<template>
    <section class="flex flex-col gap-1 w-full">
        <div :class="inputErrors.length > 0 ? 'border-red-600' : 'border-sky-600'"
            class="flex items-center w-full px-2 py-1 border border-solid rounded-md">
            <div class="relative flex justify-between items-center gap-1 w-full">
                <!-- <span v-if="inputName === 'username'">@</span> -->
                <input 
                    :id="inputId" 
                    :name="inputName" 
                    :type="inputType" 
                    :value="modelValue"
                    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
                    class="bg-transparent text-sky-800 peer focus:outline-none dark:text-white" 
                    required>
                <font-awesome-icon 
                    :icon="icon" 
                    :class="inputErrors.length > 0 ? 'text-red-600' : 'text-sky-600'" />
                <label 
                    :for="inputId"
                    class="absolute text-xs text-sky-600 transform origin-top-left translate-x-0 translate-y-0 scale-100 transition-transform pointer-events-none peer-focus:-translate-y-6 peer-focus:scale-90 peer-valid:-translate-y-6 peer-valid:scale-90"
                    :class="inputErrors.length > 0 ? 'peer-focus:text-red-600 peer-valid:text-red-600 dark:peer-focus:text-red-400 dark:peer-valid:text-red-400' : 'peer-focus:text-sky-800 peer-valid:text-sky-800 dark:peer-focus:text-sky-400 dark:peer-valid:text-sky-400'">
                    {{ labelText }}
                </label>
            </div>
        </div>
        <div class="w-48 text-xs text-red-400" v-for="error of inputErrors" :key="error.$uid">
            <span>{{ error.$message }}</span>
        </div>
    </section>
</template>