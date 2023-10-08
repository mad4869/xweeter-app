<script setup lang="ts">
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import { useDark } from '@vueuse/core'

const isDark = useDark()
</script>

<template>
    <section 
        class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Settings</span>
            <font-awesome-icon icon="fa-solid fa-gear" class="text-white" />
        </div>
        <SwitchGroup>
            <div class="flex items-center gap-2 px-4 group">
                <SwitchLabel passive>
                    <font-awesome-icon icon="fa-regular fa-sun" class="text-sky-800 dark:text-white" />
                </SwitchLabel>
                <Switch 
                    v-model="isDark"
                    class="relative inline-flex h-6 w-11 items-center bg-slate-400 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-sky-800 focus:ring-offset-2 dark:bg-sky-600">
                    <span 
                        class="inline-block h-4 w-4 transform translate-x-1 rounded-full bg-white transition-transform dark:translate-x-6" />
                </Switch>
                <SwitchLabel passive>
                    <font-awesome-icon icon="fa-regular fa-moon" class="text-sky-800 dark:text-white" />
                </SwitchLabel>
            </div>
        </SwitchGroup>
    </section>
</template>