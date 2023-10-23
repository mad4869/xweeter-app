<script setup lang="ts">
import { ref } from 'vue';

import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie } from '@/utils/axiosInstances';
import { UserResponse } from '@/types/users'
import { ToFollowResponse } from '@/types/follows'
import useFile from '@/composables/useFile'

const { userId, profilePic, headerPic, isFollowed } = defineProps<{
    isOwn: boolean,
    userId?: number,
    fullname?: string,
    username?: string,
    bio?: string | null,
    profilePic?: string,
    headerPic?: string,
    xweetsCount?: number,
    followingCount?: number,
    followersCount?: number,
    isFollowed?: boolean
}>()

const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void,
    (e: 'show-edit-profile'): void
}>()

const authStore = useAuthStore()

const pfp = ref(profilePic)
const header = ref(headerPic)
const userFollowed = ref(isFollowed)
const isLoading = ref(false)
const isEditable = ref(false)

const managePfp = async (e: Event) => {
    isEditable.value = true
    pfp.value = await useFile(e)
}

const manageHeader = async (e: Event) => {
    isEditable.value = true
    header.value = await useFile(e)
}

const changeImage = async () => {
    isLoading.value = true

    let payload

    try {
        if (pfp.value !== profilePic && header.value !== headerPic) {
            payload = { profile_pic: pfp.value, header_pic: header.value }
        } else if (pfp.value !== profilePic) {
            payload = { profile_pic: pfp.value }
        } else if (header.value !== headerPic) {
            payload = { header_pic: header.value }
        } else {
            payload = {}
        }

        const { data } = await sendReqCookie.put<UserResponse | undefined>(
            `/api/users/${userId}`, payload
        )

        if (data?.success) {
            isLoading.value = false
            isEditable.value = false

            emit('show-notice', 'success', 'Your profile images have been updated')
        }
    } catch (err) {
        isLoading.value = false
        isEditable.value = false
        pfp.value = profilePic

        emit('show-notice', 'error', 'Error occured during process. Please try again')
    }
}

const follow = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<ToFollowResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/follows/${userId}`
        )

        if (data?.success) {
            isLoading.value = false
            userFollowed.value = true
        }
    } catch (err) {
        isLoading.value = false

        emit('show-notice', 'error', 'Error occured during process. Please try again')
    }
}
</script>

<template>
    <section class="relative grid grid-rows-5 h-[50vh] rounded-lg overflow-hidden">
        <div class=" relative row-span-3 group/header">
            <img 
                :src="header" 
                class="w-full h-full object-cover"
                alt="Header" 
                loading="lazy">
            <label
                v-if="isOwn" 
                for="change-header"
                class="absolute right-4 top-4 px-2 py-1 bg-sky-600/50 backdrop-blur-md text-xs text-white font-semibold rounded-md cursor-pointer hidden group-hover/header:flex items-center hover:bg-sky-600"
                title="Change your header">
                Change
                <input 
                    type="file" 
                    id="change-header" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="manageHeader">
            </label>
        </div>
        <div class="absolute flex justify-between items-center w-full bottom-[14vh] px-12">
            <label 
                for="change-profile-pic" 
                title="Change your profile picture" 
                class="relative w-20 h-20 border border-solid border-sky-600 rounded-full shadow-xl overflow-hidden group/pfp">
                <img 
                    :src="pfp" 
                    class="w-full h-full object-cover"
                    alt="Profile Pic" 
                    loading="lazy">
                <div 
                    class="absolute left-0 top-0 w-full h-full bg-slate-600/10 backdrop-blur-sm text-xs text-white font-semibold cursor-pointer hidden group-hover/pfp:flex justify-center items-center">
                    Change
                </div>
                <input 
                    type="file" 
                    id="change-profile-pic"  
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="managePfp">
            </label>
            <div class="flex items-center gap-2">
                <button
                    v-if="isOwn"
                    class="bg-sky-600 px-4 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-md hover:bg-sky-800 hover:border-sky-600"
                    title="Edit your profile"
                    @click="$emit('show-edit-profile')">
                    Edit
                </button>
                <button
                    v-else-if="!isOwn && !userFollowed"
                    class="bg-sky-600 px-4 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-md hover:bg-sky-800 hover:border-sky-600"
                    title="Follow this user"
                    @click.prevent="follow">
                    <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
                    {{ !isLoading ? 'Follow' : '' }}
                </button>
                <div
                    v-else-if="!isOwn && userFollowed"
                    class="bg-slate-600 px-4 py-1 text-slate-400 font-medium rounded-md cursor-not-allowed"
                    title="You already followed this user">
                    Followed
                </div>
                <button
                    v-if="isEditable"
                    class="bg-sky-600 px-2 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-full"
                    title="Confirm change"
                    @click="changeImage">
                    <font-awesome-icon icon="fa-solid fa-check" class="text-sm" />
                </button>
            </div>
        </div>
        <div class="row-start-4 row-span-2 flex justify-between items-center pt-12 px-12 bg-white/10 leading-4">
            <div class="flex flex-col gap-4 max-w-[50%]">
                <div>
                    <p class="text-sky-600 font-bold">{{ fullname }}</p>
                    <p class="text-sky-800 text-sm">@{{ username }}</p>
                </div>
                <p v-if="bio" class="text-xs text-sky-800 dark:text-white">{{ bio }}</p>
            </div>
            <div class="flex flex-col justify-center items-end gap-4 text-white">
                <div>
                    <p class="text-xl"><strong>{{ xweetsCount }}</strong> <span class="text-white/50">Xweets</span></p>
                </div>
                <div class="flex justify-center items-center gap-4">
                    <p><strong>{{ followingCount }}</strong> <span class="text-white/50">Following</span></p>
                    <p><strong>{{ followersCount }}</strong> <span class="text-white/50">Followers</span></p>
                </div>
            </div>
        </div>
    </section>
</template>