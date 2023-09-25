<script setup lang="ts">
import { ref } from 'vue';
import { onClickOutside } from '@vueuse/core';

import useAuth from '../../composables/useAuth';

defineProps<{
    username: string,
    fullname: string,
    profilePic: string,
    body: string,
    fileUrl: string,
    isOwn: boolean,
    isLiked: boolean
}>()

const emit = defineEmits()

const authStore = useAuth()

const imgRef = ref<HTMLImageElement | null>(null)
const isClickedOutside = ref(false)

onClickOutside(imgRef, () => {
    isClickedOutside.value = true
    emit('clicked-outside', isClickedOutside.value)
})
</script>

<template>
    <div 
        class="fixed left-0 right-0 top-0 bottom-0 flex flex-col justify-center items-center gap-4 bg-black/5 backdrop-blur-md z-30 fade-in">
        <img 
            :src="fileUrl"
            ref="imgRef" 
            alt="Image" 
            loading="lazy" 
            class="max-w-[75vw] max-h-[75vh] border-4 border-solid border-white shadow-xl" />
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
    </div>
</template>

<style scoped>
.fade-in {
    animation: fade-in 100ms ease-in forwards;
}

@keyframes fade-in {
    from {
        opacity: 0;
    }

    to {
        opacity: 100;
    }
}
</style>