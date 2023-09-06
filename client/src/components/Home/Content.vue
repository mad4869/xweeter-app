<script setup lang="ts">
import Content from '../App/Layouts/Content.vue';
import Profile from './Profile.vue';
import SettingBar from '../App/SettingBar.vue';
import Suggestions from '../App/Suggestions.vue';
import NewZweet from './NewZweet.vue';
import Sep from './Sep.vue';
import Zweet from '../App/Zweet.vue';

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
    <Content>
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
    </Content>
</template>

<style scoped></style>