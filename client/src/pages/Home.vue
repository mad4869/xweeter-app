<script setup lang="ts">
import Layout from '../components/App/Layout/index.vue'
import SettingBar from '../components/App/SettingBar.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Xweet from '../components/App/Xweet.vue';
import NewZweet from '../components/Home/NewZweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import useAuth from '../composables/useAuth';
import apiRequest from '../utils/apiRequest';

type Xweets = {
    xweet_id: number,
    user_id: number,
    full_name: string,
    username: string,
    body: string,
    media?: string,
    profile_pic: string,
    created_at: string,
    updated_at?: string
}

type Response = {
    data: Xweets[],
    success: boolean
}

const authStore = useAuth()
await authStore.getUser()

const getTimeline = async (): Promise<Response | undefined> => {
    try {
        const { data } = await apiRequest.get(`/api/users/${authStore.getSignedInUserId}/timeline`)
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getTimeline()) || { data: [] }
</script>

<template>
    <Layout>
        <template v-slot:sidebarLeft>
            <Profile />
            <SettingBar />
        </template>
        <NewZweet />
        <Sep title="Timeline" />
        <Xweet v-for="xweet in data" :key="xweet.xweet_id" :fullname="xweet.full_name" :username="xweet.username"
            :body="xweet.body" :profilePic="xweet.profile_pic" :createdAt="xweet.created_at" :is-rexweet="false" />
        <template v-slot:sidebarRight>
            <Suggestions />
        </template>
    </Layout>
</template>
