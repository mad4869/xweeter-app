<script setup lang="ts">
import Xweet from '../App/Xweet.vue';
import useAuth from '../../composables/useAuth';
import apiRequest from '../../utils/apiRequest';

type Xweets = {
    xweet_id: number,
    user_id: number,
    rexweet_id?: number,
    full_name?: string,
    username?: string,
    body: string,
    media?: string,
    profile_pic?: string,
    created_at: string,
    updated_at?: string,
    og_user_id?: number,
    og_username?: string,
    og_full_name?: string,
    og_profile_pic?: string
}

type Response = {
    data: Xweets[],
    success: boolean
}

const authStore = useAuth()
await authStore.getUser()

const getProfileTimeline = async (): Promise<Response | undefined> => {
    try {
        const { data } = await apiRequest.get(`api/users/${authStore.getSignedInUserId}/profile-timeline`)
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getProfileTimeline()) || { data: [] }
</script>

<template>
    <section class="flex flex-col gap-4">
        <Xweet v-for="xweet in data" :key="xweet.xweet_id" 
            :fullname="xweet.full_name" 
            :username="xweet.username"
            :body="xweet.body"
            :profilePic="xweet.profile_pic" 
            :createdAt="xweet.created_at"
            :isRexweet="xweet.rexweet_id !== undefined"
            :og_username="xweet.og_username"
            :og_fullname="xweet.og_full_name"
            :og_profile_pic="xweet.og_profile_pic" />
    </section>
</template>