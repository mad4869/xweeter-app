<script setup lang="ts">
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';

type User = {
    user_id: number,
    username: string,
    full_name: string,
    email: string,
    bio: string | null,
    role: 'admin' | 'user',
    profile_pic: string,
    header_pic: string,
    created_at: string,
    updated_at: string | null
}

type Response = {
    success: boolean,
    data: User[]
}

const authStore = useAuth()
await authStore.getUser()

const queryFollow = async (): Promise<Response[] | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const following = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/following`)
            const followers = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/followers`)
            if (following.data && followers.data) {
                return [following.data, followers.data]
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const data = (await queryFollow()) || []
</script>

<template>
    <section class="flex-[2] flex flex-col justify-evenly items-center border border-solid border-sky-800 rounded-xl">
        <div class="flex justify-center items-center gap-4 w-full px-8 pb-4 border-b border-solid border-sky-600/20">
            <div>
                <img :src="authStore.getSignedInPfp" class="w-12 h-12 border border-solid border-sky-800 rounded-full" />
            </div>
            <div class="flex flex-col">
                <span class="text-white font-bold">{{ authStore.getSignedInFullname }}</span>
                <span class="text-sm text-sky-800">@{{ authStore.getSignedInUsername }}</span>
            </div>
        </div>
        <div
            class="flex justify-center items-center gap-2 w-full pb-4 text-white text-lg border-b border-solid border-sky-600/20">
            <span class="font-bold">1150</span>
            <span>Zweets</span>
        </div>
        <div class="flex flex-col items-center w-full pb-4 text-white text-lg border-b border-solid border-sky-600/20">
            <span><strong>{{ data[0].data.length }}</strong> Followings</span>
            <span><strong>{{ data[1].data.length }}</strong> Followers</span>
        </div>
        <div>
            <input type="button" value="New Zweet" class="px-4 py-2 bg-sky-600 text-white text-lg font-bold rounded-xl">
        </div>
    </section>
</template>