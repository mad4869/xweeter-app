<script setup lang="ts">
import { ref } from 'vue';

import { sendReqCookie } from '../../utils/axiosInstances';
import { UserResponse } from '../../types/users'



const { userId, profilePic, headerPic } = defineProps<{
    isOwn: boolean,
    userId?: number,
    fullname?: string,
    username?: string,
    bio?: string | null,
    profilePic?: string,
    headerPic?: string
}>()

const emit = defineEmits<{
    (e: 'change-profile-pic', isSuccess: boolean, isError: boolean, NotifMsg: string): void,
    (e: 'show-edit-profile'): void
}>()

const pfp = ref(profilePic)
const header = ref(headerPic)
const isSuccess = ref(false)
const isError = ref(false)
const isLoading = ref(false)
const isEditable = ref(false)
const notifMsg = ref('')

const managePfp = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        isEditable.value = true

        const reader = new FileReader()

        reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target instanceof FileReader) {
                pfp.value = e.target.result as string
            }
        }

        reader.readAsDataURL(file)
    }
}

const manageHeader = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        isEditable.value = true

        const reader = new FileReader()

        reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target instanceof FileReader) {
                header.value = e.target.result as string
            }
        }

        reader.readAsDataURL(file)
    }
}

// const changeProfilePic = async () => {
//     isLoading.value = true

//     try {
//         const { data } = await sendReqCookie.put<UserResponse | undefined>(
//             `/api/users/${userId}`, { profile_pic: pfp.value }
//         )

//         if (data?.success) {
//             isLoading.value = false
//             isSuccess.value = true
//             isEditable.value = false
//             notifMsg.value = 'Your profile picture has been changed'
//             emit('change-profile-pic', isSuccess.value, isError.value, notifMsg.value)

//             setTimeout(() => {
//                 isSuccess.value = false
//             }, 3000)
//         }
//     } catch (err) {
//         isLoading.value = false
//         isEditable.value = false
//         isError.value = true
//         pfp.value = profilePic
//         notifMsg.value = 'Error occured during process. Please try again.'
//         emit('change-profile-pic', isSuccess.value, isError.value, notifMsg.value)

//         setTimeout(() => {
//             isError.value = false
//         }, 3000)

//         console.error(err)
//     }
// }

const changeHeader = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<UserResponse | undefined>(
            `/api/users/${userId}`, { header_pic: header.value }
        )

        if (data?.success) {
            // isLoading.value = false
            isSuccess.value = true
            isEditable.value = false
            notifMsg.value = 'Your profile picture has been changed'
            emit('change-profile-pic', isSuccess.value, isError.value, notifMsg.value)

            setTimeout(() => {
                isSuccess.value = false
            }, 3000)
        }
    } catch (err) {
        // isLoading.value = false
        // isEditable.value = false
        // isError.value = true
        // pfp.value = profilePic
        // notifMsg.value = 'Error occured during process. Please try again.'
        // emit('change-profile-pic', isSuccess.value, isError.value, notifMsg.value)

        // setTimeout(() => {
        //     isError.value = false
        // }, 3000)

        console.error(err)
    }
}

const showEditProfile = () => {
    emit('show-edit-profile')
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
                    class="w-full h-full"
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
                    @click.prevent="showEditProfile">
                    Edit
                </button>
                <button
                    v-else
                    class="bg-sky-600 px-4 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-md">
                    Follow
                </button>
                <button
                    v-if="isEditable"
                    class="bg-sky-600 px-2 py-1 text-white font-medium border-2 border-solid border-sky-800 rounded-full"
                    title="Confirm change"
                    @click.prevent="changeHeader">
                    <font-awesome-icon icon="fa-solid fa-check" class="text-sm" />
                </button>
            </div>
        </div>
        <div class="row-start-4 row-span-2 flex flex-col gap-4 pt-12 px-12 bg-white/10 leading-4">
            <div>
                <p class="text-sky-600 font-bold">{{ fullname }}</p>
                <p class="text-sky-800 text-sm">@{{ username }}</p>
            </div>
            <p v-if="bio" class="text-xs text-sky-800 dark:text-white">{{ bio }}</p>
        </div>
    </section>
</template>