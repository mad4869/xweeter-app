<script setup lang="ts">
import Layout from '../components/App/Layout/index.vue'
import Title from '../components/Leaderboard/Title.vue';
import Table from '../components/Leaderboard/Table.vue';
import { sendReqCookie } from '../utils/axiosInstances';

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
        const { data } = await sendReqCookie.get('/api/users/1/xweets')
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
        <Title />
        <Table users="@Aconitin" :xweets-count="data.length" />
    </Layout>
</template>