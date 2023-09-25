<script setup lang="ts">
import { ref } from 'vue';

import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';
import { UserResponse } from '../../types/users'

const authStore = useAuth()

const emit = defineEmits()

const profile_pic = ref(authStore.getSignedInPfp)
const isSuccess = ref(false)
const isError = ref(false)
const isLoading = ref(false)
const notifMsg = ref('')

const manageFile = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target instanceof FileReader) {
                profile_pic.value = e.target.result as string
            }
        }

        reader.readAsDataURL(file)
    }
}

const changeProfilePic = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<UserResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}`, { profile_pic: profile_pic.value }
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            notifMsg.value = 'Your profile picture has been changed'
            emit('change-profile-pic', isSuccess.value, isError.value, notifMsg.value)

            setTimeout(() => {
                isSuccess.value = false
            }, 3000)
        }
    } catch (err) {
        isLoading.value = false
        isError.value = true
        profile_pic.value = authStore.getSignedInPfp
        notifMsg.value = 'Error occured during process. Please try again.'
        emit('change-profile-pic', isSuccess.value, isError.value, notifMsg.value)

        setTimeout(() => {
            isError.value = false
        }, 3000)

        console.error(err)
    }
}
</script>

<template>
    <section class="relative grid grid-rows-5 h-[50vh] rounded-lg overflow-hidden">
        <div class="row-span-3">
            <img 
                :src="authStore.getSignedInHeader" 
                class="w-full h-full object-cover"
                alt="Header" 
                loading="lazy">
        </div>
        <div class="absolute flex justify-between items-center w-full bottom-[14vh] px-12">
            <label 
                for="change-profile-pic" 
                title="Change your profile picture" 
                class="relative w-20 h-20 border border-solid border-sky-600 rounded-full shadow-xl overflow-hidden group">
                <img 
                    :src="profile_pic" 
                    class="w-full h-full"
                    alt="Profile Pic" 
                    loading="lazy">
                <div 
                    class="absolute left-0 top-0 w-full h-full bg-slate-600/10 backdrop-blur-sm text-xs text-white font-semibold cursor-pointer hidden group-hover:flex justify-center items-center">
                    Change
                </div>
                <input 
                    type="file" 
                    id="change-profile-pic" 
                    alt="Add Image" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="manageFile">
            </label>
            <button
                class="bg-sky-600 px-4 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-md">
                Follow
            </button>
        </div>
        <div class="row-start-4 row-span-2 flex flex-col gap-4 pt-12 px-12 bg-white/10 leading-4">
            <div>
                <p class="text-sky-600 font-bold">{{ authStore.getSignedInFullname }}</p>
                <p class="text-sky-800 text-sm">@{{ authStore.getSignedInUsername }}</p>
            </div>
            <p class="text-xs text-sky-800 dark:text-white">{{ authStore.getSignedInBio }}</p>
            <button @click.prevent="changeProfilePic">Change Profile Picture</button>
        </div>
    </section>
</template>