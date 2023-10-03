<script setup lang="ts">
import Layout from '../components/App/Layout/index.vue'
import Sep from '../components/Home/Sep.vue';
import Table from '../components/Leaderboard/Table.vue';
import { sendReqWoCookie } from '../utils/axiosInstances';
import { TopDailyResponse } from '../types/users'

const queryTopDailyUsers = async (): Promise<TopDailyResponse | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get('/api/users/most-active-daily')
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await queryTopDailyUsers()) || { data: [] }
</script>

<template>
    <Layout>
        <Sep is-sticky title="Top Daily Users" />
        <Table :data="data" />
    </Layout>
</template>