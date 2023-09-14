<script setup lang="ts">
import axios from 'axios';

import Zweet from '../../components/App/Zweet.vue';

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
    try {
        const { data } = await axios.get('http://localhost:5000/api/users/1/xweets')
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
    <section class="flex flex-col gap-4">
        <Zweet v-for="xweet in data" :key="xweet.xweet_id" 
            :fullname="xweet.full_name" 
            :username="xweet.username"
            :body="xweet.body"
            :profilePic="xweet.profile_pic" 
            :createdAt="xweet.created_at" />
    </section>
</template>