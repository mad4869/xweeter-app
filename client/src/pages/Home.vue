<script setup lang="ts">
import Layout from '../components/App/Layout/index.vue'
import SettingBar from '../components/App/SettingBar.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Zweet from '../components/App/Zweet.vue';
import NewZweet from '../components/Home/NewZweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import apiRequest from '../utils/apiRequest';

type Xweet = {
    xweet_id: number,
    user_id: number,
    full_name: string,
    username: string,
    body: string,
    profile_pic: string,
    created_at: string,
    updated_at: string | null
}

type Response = {
    data: Xweet[],
    success: boolean
}

const queryXweets = async (): Promise<Response | undefined> => {
    try {
        const { data } = await apiRequest.get('/api/users/1/xweets')
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await queryXweets()) || { data: [] }
</script>

<template>
    <Layout>
        <template v-slot:sidebarLeft>
            <Profile />
            <SettingBar />
        </template>
        <NewZweet />
        <Sep title="Timeline" />
        <Zweet v-for="xweet in data" :key="xweet.xweet_id" :fullname="xweet.full_name" :username="xweet.username"
            :body="xweet.body" :profilePic="xweet.profile_pic" :createdAt="xweet.created_at" />
        <template v-slot:sidebarRight>
            <Suggestions />
        </template>
    </Layout>
</template>
