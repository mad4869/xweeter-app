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
    <section class="flex flex-col gap-1">
        <div :class="inputErrors.length > 0 ? 'border-red-600' : 'border-sky-600'"
            class="flex items-center px-2 py-2 border border-solid rounded-md">
            <div class="relative flex justify-between items-center gap-1">
                <input :id="inputId" :name="inputName" :type="inputType" :value="modelValue"
                    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
                    class="bg-transparent text-white peer focus:outline-none" required>
                <font-awesome-icon 
                    :icon="icon" 
                    :class="inputErrors.length > 0 ? 'text-red-600' : 'text-sky-600'" />
                <label :for="inputId"
                    class="absolute text-xs text-slate-400 transform origin-top-left translate-x-0 translate-y-0 scale-100 transition-transform pointer-events-none peer-focus:-translate-y-8 peer-focus:scale-90 peer-valid:-translate-y-8 peer-valid:scale-90"
                    :class="inputErrors.length > 0 ? 'peer-focus:text-red-400 peer-valid:text-red-400' : 'peer-focus:text-sky-600 peer-valid:text-sky-600'">
                    {{ labelText }}
                </label>
            </div>
        </div>
        <div class="w-48 text-xs text-red-400" v-for="error of inputErrors" :key="error.$uid">
            <span>{{ error.$message }}</span>
        </div>
    </section>
</template>

<style scoped>
.error {
    @apply border-red-400
}
</style>