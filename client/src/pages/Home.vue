<script setup lang="ts">
import Layout from '../components/App/Layout/index.vue'
import SettingBar from '../components/App/SettingBar.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Zweet from '../components/App/Zweet.vue';
import NewZweet from '../components/Home/NewZweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';

const contents = [
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
]
</script>

<template>
    <Layout>
        <template v-slot:sidebarLeft>
            <Profile />
            <SettingBar />
        </template>
        <NewZweet />
        <Sep title="Timeline" />
        <Zweet v-for="(content, index) in contents" :key="index" :fullname="content.fullname" :username="content.username"
            :zweet="content.zweet" />
        <template v-slot:sidebarRight>
            <Suggestions />
        </template>
    </Layout>
</template>
