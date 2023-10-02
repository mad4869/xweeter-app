<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';

import Layout from '../components/App/Layout/index.vue'
import Toggle from '../components/App/Toggle.vue';
import SigninForm from '../components/App/SigninForm.vue';
import SignupForm from '../components/App/SignupForm.vue';
import Setting from '../components/App/Setting.vue';
import Suggestions from '../components/App/Suggestions.vue';
import Trending from '../components/App/Trending.vue';
import Xweet from '../components/App/Xweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import useAuth from '../composables/useAuth';
import { UserAuth } from '../types/auth';
import { XweetResponse } from '../types/xweets';
import { RepliesResponse } from '../types/replies'
import { sendReqWoCookie } from '../utils/axiosInstances';

const authStore = useAuth()
await authStore.getUser()

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}

const route = useRoute()

const getXweet = async (): Promise<XweetResponse | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get(`/api/xweets/${route.params.id}`)
            if (data) {
                return data
            }
    } catch (err) {
        console.error(err)
    }
}

const getReplies = async (): Promise<RepliesResponse | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get(`/api/xweets/${route.params.id}/replies`)
            if (data) {
                return data
            }
    } catch (err) {
        console.error(err)
    }
}

const xweet = (await getXweet()) || { data: undefined }
const { data } = (await getReplies()) || { data: [] }
</script>

<template>
    <Layout>
        <template #sidebarLeft>
            <section 
                v-if="!authStore.getIsAuthenticated"
                class="flex-[4] flex flex-col items-center px-2 pt-4 border border-solid border-sky-800 rounded-xl">
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
        <Sep :title="`Xweet from: @${xweet.data?.username}`" />
        <Xweet
            :key="xweet.data?.xweet_id"
            :id="xweet.data?.xweet_id!"
            :userId="xweet.data?.user_id!"
            :fullname="xweet.data?.full_name!" 
            :username="xweet.data?.username!" 
            :body="xweet.data?.body!" 
            :media="xweet.data?.media"
            :profilePic="xweet.data?.profile_pic" 
            :createdAt="xweet.data?.created_at!" 
            :updated-at="xweet.data?.updated_at" 
            :is-rexweet="false"
            :is-own="xweet.data?.user_id === authStore.getSignedInUserId" 
            :rexweeted="false"
            :liked="false" />
        <Xweet v-for="reply in data"
            :key="reply.xweet_id"
            :id="reply.xweet_id!"
            :userId="reply.user_id!"
            :fullname="reply.full_name!" 
            :username="reply.username!" 
            :body="reply.body!" 
            :media="reply.media"
            :profilePic="reply.profile_pic" 
            :createdAt="reply.created_at!" 
            :updated-at="reply.updated_at" 
            :is-rexweet="false"
            :is-own="reply.user_id === authStore.getSignedInUserId" 
            :rexweeted="false"
            :liked="false" />
        <template #sidebarRight>
            <Suggestions v-if="authStore.getIsAuthenticated" />
            <Trending />
        </template>
    </Layout>
</template>