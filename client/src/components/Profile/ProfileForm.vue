<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required, email as isEmail } from '@vuelidate/validators'

import InputField from '@/components/App/InputField.vue';
import { sendReqCookie } from '@/utils/axiosInstances';
import { UserResponse } from '@/types/users';
import useFile from '@/composables/useFile';

const { userId, username, fullname, email, bio, profilePic, headerPic } = defineProps<{
    userId?: number,
    username?: string,
    fullname?: string,
    email?: string,
    bio?: string | null,
    profilePic?: string,
    headerPic?: string
}>()
const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void
    (e: 'close-modal'): void
}>()

const userProfile = reactive({
    username,
    fullname,
    email,
    bio,
    profile_pic: profilePic,
    header_pic: headerPic
})

const rules = {
    username: { required },
    fullname: { required },
    email: { required, isEmail },
    bio: {}
}

const v$ = useVuelidate(rules, userProfile)

const isLoading = ref(false)

const editProfilePic = async (e: Event) => {
    userProfile.profile_pic = await useFile(e)
}

const editHeader = async (e: Event) => {
    userProfile.header_pic = await useFile(e)
}

const editProfile = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<UserResponse | undefined>(
            `/api/users/${userId}`, userProfile
        )

        if (data?.success) {
            isLoading.value = false

            emit('close-modal')
            emit('show-notice', 'success', 'Your profile has been updated')
        }
    } catch (err) {
        isLoading.value = false

        emit('close-modal')
        emit('show-notice', 'error', 'Error occured during process. Please try again')
    }
}
</script>

<template>
    <form 
        class="flex flex-col justify-center items-center gap-6 px-8 py-4 min-w-[50%]"
        @submit.prevent="editProfile">
        <h3 class="text-2xl text-white font-semibold">Edit Profile</h3>
        <InputField 
            input-id="fullname" 
            input-name="fullname" 
            input-type="text" 
            :input-errors="v$.fullname.$errors"
            v-model="v$.fullname.$model" 
            label-text="Full Name" 
            icon="fa-solid fa-font" />
        <InputField 
            input-id="username" 
            input-name="username" 
            input-type="text" 
            :input-errors="v$.username.$errors"
            v-model="v$.username.$model" 
            label-text="Username" 
            icon="fa-solid fa-user" />
        <InputField
            input-id="email"
            input-name="email"
            input-type="text"
            :input-errors="v$.email.$errors"
            v-model="v$.email.$model"
            label-text="Email"
            icon="fa-solid fa-envelope" />
        <InputField
            input-id="bio"
            input-name="bio"
            input-type="text"
            v-model="v$.bio.$model"
            label-text="Bio"
            icon="fa-solid fa-address-card" />
        <div class="flex justify-between items-center w-full">
            <label for="edit-profile-pic" title="Change your profile picture">
                <span
                    class="flex items-center gap-2 px-2 py-1 bg-sky-800/50 text-xs text-white rounded-md transition-colors cursor-pointer hover:bg-sky-800 dark:bg-sky-400/50 dark:hover:bg-sky-400">
                    <font-awesome-icon icon="fa-solid fa-image-portrait" />
                    <h6>Profile Picture</h6>
                </span>
                <input 
                    type="file" 
                    id="edit-profile-pic" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="editProfilePic">
            </label>
            <div v-if="userProfile.profile_pic" class="relative group">
                <img :src="userProfile.profile_pic" class="w-8 h-8 object-scale-down" />
                <font-awesome-icon 
                    icon="fa-regular fa-circle-xmark" 
                    title="Remove the image"
                    class="absolute -top-1 -right-1 text-xs text-sky-800 cursor-pointer dark:text-white hidden group-hover:block"
                    @click="userProfile.profile_pic = ''" />
            </div>
        </div>
        <div class="flex justify-between items-center w-full">
            <label for="edit-header" title="Change your header">
                <span
                    class="flex items-center gap-2 px-2 py-1 bg-sky-800/50 text-xs text-white rounded-md transition-colors cursor-pointer hover:bg-sky-800 dark:bg-sky-400/50 dark:hover:bg-sky-400">
                    <font-awesome-icon icon="fa-solid fa-panorama" />
                    <h6>Header</h6>
                </span>
                <input 
                    type="file" 
                    id="edit-header" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="editHeader">
            </label>
            <div v-if="userProfile.header_pic" class="relative group">
                <img :src="userProfile.header_pic" class="w-8 h-8 object-scale-down" />
                <font-awesome-icon 
                    icon="fa-regular fa-circle-xmark" 
                    title="Remove the image"
                    class="absolute -top-1 -right-1 text-xs text-sky-800 cursor-pointer dark:text-white hidden group-hover:block"
                    @click="userProfile.header_pic = ''" />
            </div>
        </div>
        <button 
            type="submit"
            class="uppercase w-24 py-1 bg-sky-600 text-white rounded-md shadow-sm shadow-slate-900/50 transition-colors duration-200 ease-in hover:bg-sky-800 active:shadow-inner disabled:bg-neutral-800 disabled:text-neutral-600 disabled:shadow-none disabled:cursor-not-allowed"
            title="Fix your profile"
            :disabled="v$.$invalid">
            <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
            {{ !isLoading ? 'Submit' : '' }}
        </button>
    </form>
</template>