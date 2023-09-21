<script setup lang="ts">
import { ref } from 'vue';
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'

import useTheme from '../../composables/useTheme';

const themeStore = useTheme()

const darkModeEnabled = ref(false)
if (darkModeEnabled) {
    themeStore.resetToDark()
} else {
    themeStore.switchToLight()
}
</script>

<template>
    <section class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Settings</span>
            <font-awesome-icon icon="fa-solid fa-gear" class="text-white" />
        </div>
        <SwitchGroup>
            <div class="flex items-center gap-2 px-4 group">
                <SwitchLabel passive>
                    <font-awesome-icon icon="fa-regular fa-sun" class="text-white" />
                </SwitchLabel>
                <Switch v-model="darkModeEnabled"
                    class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    :class="darkModeEnabled ? 'bg-sky-600' : 'bg-slate-400'">
                    <span class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
                        :class="darkModeEnabled ? 'translate-x-6' : 'translate-x-1'" />
                </Switch>
                <SwitchLabel passive>
                    <font-awesome-icon icon="fa-regular fa-moon" class="text-white" />
                </SwitchLabel>
            </div>
        </SwitchGroup>
    </section>
</template>