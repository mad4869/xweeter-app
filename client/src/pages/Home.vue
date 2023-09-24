<script setup lang="ts">
import { ref, reactive } from 'vue';

import Layout from '../components/App/Layout/index.vue'
import Setting from '../components/App/Setting.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Xweet from '../components/App/Xweet.vue';
import NewXweet from '../components/Home/NewXweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import SigninForm from '../components/App/SigninForm.vue';
import SignupForm from '../components/App/SignupForm.vue';
import Toggle from '../components/App/Toggle.vue';
import Trending from '../components/App/Trending.vue';
import useAuth from '../composables/useAuth';
import { UserAuth } from '../types/auth';
import { Xweets, XweetsResponse } from '../types/xweets';
import socket from '../utils/socket';
import { sendReqCookie, sendReqWoCookie } from '../utils/axiosInstances';

const authStore = useAuth()
await authStore.getUser()

const getTimeline = async (): Promise<XweetsResponse | undefined> => {
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

const timeline = reactive<Xweets[]>(data)
socket.on('timeline', (xweet) => {
    timeline.unshift(xweet)
})

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}
</script>

<template>
    <Layout>
        <template #sidebarLeft>
            <section
                class="flex-[4] flex flex-col items-center px-2 pt-4 border border-solid border-sky-800 rounded-xl"
                v-if="!authStore.getIsAuthenticated">
                <Toggle :active-btn="activeBtn" @activate-btn="activateBtn" />
                <Transition name="fade" mode="out-in">
                    <KeepAlive>
                        <SignupForm :use-title="false" v-if="activeBtn === UserAuth.SignUp" />
                        <SigninForm :use-title="false" v-else />
                    </KeepAlive>
                </Transition>
            </section>
            <Profile v-if="authStore.getIsAuthenticated" />
            <Setting />
        </template>
        <NewXweet v-if="authStore.getIsAuthenticated" />
        <Sep title="Timeline" />
        <Xweet 
            v-for="xweet in timeline" 
            :key="xweet.xweet_id"
            :id="xweet.xweet_id"
            :user_id="xweet.user_id" 
            :fullname="xweet.full_name" 
            :username="xweet.username"
            :body="xweet.body"
            :media="xweet.media" 
            :profilePic="xweet.profile_pic" 
            :createdAt="xweet.created_at" 
            :is-rexweet="false" />
        <template #sidebarRight>
            <Suggestions v-if="authStore.getIsAuthenticated" />
            <Trending />
        </template>
    </Layout>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    @apply transition-all duration-300 ease-out
}

.fade-enter-from,
.fade-leave-to {
    @apply translate-x-4 opacity-0
}
</style>