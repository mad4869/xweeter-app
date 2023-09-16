<script setup lang="ts">
import axios from 'axios';

import useAuth from '../../composables/useAuth';
import getCookie from '../../utils/getCookie';

type Following = {
    following_id: number,
    followed_id: number,
    follower_id: number,
    username: string,
    full_name: string,
    profile_pic: string,
    bio: string | null,
    created_at: string,
    updated_at: string | null
}

type Response = {
    success: boolean,
    data: Following[]
}

const authStore = useAuth()
await authStore.getUser()

const queryFollow = async (): Promise<Response | undefined> => {
    const OPTIONS = {
        credentials: 'same-origin',
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    }

    try {
        const { data } = await axios.get(`/api/users/${authStore.getSignedInUserId}/following`, OPTIONS)
        if (data) {
            console.log(data)
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await queryFollow()) || { data: [] }
</script>

<template>
    <section class="flex-[2] flex flex-col justify-evenly items-center border border-solid border-sky-800 rounded-xl">
        <div class="flex justify-between items-center w-full px-8 pb-4 border-b border-solid border-sky-600/20">
            <div>
                <img :src="authStore.getSignedInPfp" class="w-10 h-10 border border-solid border-sky-800 rounded-full" />
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
            <span><strong>{{ data.length }}</strong> Followings</span>
            <span><strong>650</strong> Followers</span>
        </div>
        <div>
            <input type="button" value="New Zweet" class="px-4 py-2 bg-sky-600 text-white text-lg font-bold rounded-xl">
        </div>
    </section>
</template>