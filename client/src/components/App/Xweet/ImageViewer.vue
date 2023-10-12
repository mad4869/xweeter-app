<script setup lang="ts">
import { ref } from 'vue';
import { onClickOutside } from '@vueuse/core';

import useAuthStore from '@/stores/useAuthStore';
import { TransitionRoot } from '@headlessui/vue';

defineProps<{
    show: boolean
    username: string
    fullname: string
    profilePic: string
    body: string
    fileUrl?: string
    isOwn: boolean
    isLiked: boolean
}>()

const emit = defineEmits<{
    (e: 'clicked-outside'): void
}>()

const authStore = useAuthStore()

const imgRef = ref<HTMLDivElement | null>(null)

onClickOutside(imgRef, () => {
    emit('clicked-outside')
})
</script>

<template>
    <TransitionRoot
        :show="show"
        as="div" 
        class="fixed left-0 right-0 top-0 bottom-0 flex flex-col justify-center items-center gap-4 bg-black/5 backdrop-blur-md z-30"
        enter="transition-opacity ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0">
        <div class="relative group" ref="imgRef">
            <img 
                :src="fileUrl" 
                alt="Image" 
                loading="lazy" 
                class="max-w-[75vw] max-h-[75vh] border-4 border-solid border-white shadow-xl" />
            <div class="absolute items-center -right-4 -top-4 w-8 h-8 px-2 py-2 bg-white/50 rounded-full hidden group-hover:flex hover:bg-white">
                <a :href="fileUrl" class="text-sky-800" title="Download this image" download>
                    <font-awesome-icon 
                        icon="fa-solid fa-download" />
                </a>
            </div>
        </div>
        <div 
            class="flex justify-center items-center gap-4 w-[50vw] px-8 py-2 bg-slate-900/70 text-white rounded-lg">
            <aside class="flex justify-center items-center">
                <img 
                    :src="profilePic" 
                    alt="Profile Pic"
                    class="w-10 h-10 border border-solid border-sky-800 rounded-full" 
                    loading="lazy">
            </aside>
            <div class="flex-1 flex flex-col items-center">
                <div class="flex justify-between items-center w-full">
                    <div class="flex gap-2 text-sm text-sky-400">
                        <span class="font-bold">{{ fullname }}</span>
                        <span>@{{ username }}</span>
                    </div>
                    <div class="flex justify-center items-center gap-4">
                        <font-awesome-icon 
                            v-if="authStore.getIsAuthenticated && !isOwn"
                            icon="fa-solid fa-retweet" 
                            class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                            title="Rexweet" />
                        <font-awesome-icon 
                            v-if="authStore.getIsAuthenticated && !isLiked"
                            icon="fa-regular fa-heart"
                            class="text-sm transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                            title="Like Xweet" />
                        <font-awesome-icon
                            v-if="authStore.getIsAuthenticated && isLiked"
                            icon="fa-solid fa-heart"
                            class="text-sm transition-transform cursor-pointer text-sky-600 scale-105"
                            title="Unlike Xweet" />
                        <font-awesome-icon
                            v-if="authStore.getIsAuthenticated && isOwn"
                            icon="fa-regular fa-trash-can"
                            class="text-sm transition-transform cursor-pointer hover:text-red-600 hover:scale-105"
                            title="Delete Xweet"/>
                    </div>
                </div>
                <span class="w-full">{{ body }}</span>
            </div>
        </div>
    </TransitionRoot>
</template>