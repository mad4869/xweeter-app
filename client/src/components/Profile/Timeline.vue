<script setup lang="ts">
import Xweet from '../App/Xweet.vue';
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';

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

const getProfileTimeline = async (): Promise<Response | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(`api/users/${authStore.getSignedInUserId}/profile-timeline`)
            if (data) {
                return data
            }
        } else {
            return { data: [], success: false }
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getProfileTimeline()) || { data: [] }
</script>

<template>
    <section class="flex flex-col gap-4">
        <Xweet 
            v-for="xweet in data" 
            :key="xweet.xweet_id" 
            :id="xweet.xweet_id"
            :userId="xweet.user_id"
            :fullname="xweet.full_name" 
            :username="xweet.username"
            :body="xweet.body" 
            :profilePic="xweet.profile_pic" 
            :createdAt="xweet.created_at"
            :isRexweet="xweet.rexweet_id !== undefined" 
            :og_username="xweet.og_username" 
            :og_fullname="xweet.og_full_name"
            :og_profile_pic="xweet.og_profile_pic"
            :isOwn="true"
            :rexweeted="false"
            :liked="false" />
    </section>
</template>