<script setup lang="ts">
import axios from 'axios'

import Layout from '../components/App/Layout/index.vue'
import SettingBar from '../components/App/SettingBar.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Zweet from '../components/App/Zweet.vue';
import NewZweet from '../components/Home/NewZweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import getCookie from '../utils/getCookie'

type Xweet = {
    xweet_id: number,
    user_id: number,
    full_name: string,
    username: string,
    body: string,
    profile_pic: string,
    created_at: string,
    updated_at: string
}

type Response = {
    data: Xweet[],
    success: boolean
}

const queryXweets = async (): Promise<Response | undefined> => {
    const OPTIONS = {
        credentials: 'same-origin',
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    }

    try {
        const { data } = await axios.get('http://localhost:5000/api/users/1/xweets', OPTIONS)
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
