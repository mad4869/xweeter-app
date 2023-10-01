<script setup lang="ts">
import { sendReqCookie } from '../../utils/axiosInstances';
import UserToFollow from './UserToFollow.vue';

type WhoToFollow = {
    user_id: number,
    username: string,
    full_name: string,
    body: string,
    profile_pic: string
}

type WhoToFollowResponse = {
    data: WhoToFollow[],
    success: boolean
}

const getActiveUsers = async (): Promise<WhoToFollowResponse | undefined> => {
    try {
        const { data } = await sendReqCookie.get('/api/users/most-active')
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getActiveUsers()) || { data: [] }
</script>

<template>
    <section 
        class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Who to Follow</span>
            <font-awesome-icon icon="fa-regular fa-user" class="text-white" />
        </div>
        <div class="flex flex-col justify-center gap-2 overflow-scroll">
            <UserToFollow
                v-for="user in data" 
                :key="user.user_id"
                :id="user.user_id" 
                :fullname="user.full_name" 
                :username="user.username"
                :last-xweet="user.body"
                :profile-pic="user.profile_pic" />
        </div>
    </section>
</template>