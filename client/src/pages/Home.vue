<script setup lang="ts">
import Layout from '../components/App/Layout/index.vue'
import Setting from '../components/App/Setting.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Xweet from '../components/App/Xweet.vue';
import NewXweet from '../components/Home/NewXweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import SigninForm from '../components/App/SigninForm.vue';
// import SignupForm from '../components/App/SignupForm.vue';
import Toggle from '../components/App/Toggle.vue';
import useAuth from '../composables/useAuth';
import { UserAuth } from '../types/auth';
import { sendReqCookie, sendReqWoCookie } from '../utils/axiosInstances';
import Trending from '../components/App/Trending.vue';

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
try {
    await authStore.getUser()
} catch (err) {
    console.error(err)
}

const getTimeline = async (): Promise<Response | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/timeline`)
            if (data) {
                return data
            }
        } else {
            const { data } = await sendReqWoCookie.get(`/api/timeline`)
            if (data) {
                return data
            }
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
            <section
                class="flex-[2] flex flex-col justify-evenly items-center border border-solid border-sky-800 rounded-xl">
                <Toggle v-if="!authStore.getIsAuthenticated" :active-btn="UserAuth.SignIn" @activate-btn="() => ''" />
                <!-- <SignupForm :use-title="false" v-if="!authStore.getIsAuthenticated" /> -->
                <SigninForm :use-title="false" v-if="!authStore.getIsAuthenticated" />
            </section>
            <Profile v-if="authStore.getIsAuthenticated" />
            <Setting />
        </template>
        <NewXweet v-if="authStore.getIsAuthenticated" />
        <Sep title="Timeline" />
        <Xweet v-for="xweet in data" :key="xweet.xweet_id" :fullname="xweet.full_name" :username="xweet.username"
            :body="xweet.body" :profilePic="xweet.profile_pic" :createdAt="xweet.created_at" :is-rexweet="false" />
        <template v-slot:sidebarRight>
            <Suggestions v-if="authStore.getIsAuthenticated" />
            <Trending />
        </template>
    </Layout>
</template>