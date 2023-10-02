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
import { XweetsResponse } from '../types/xweets';
import { sendReqWoCookie } from '../utils/axiosInstances';

const authStore = useAuth()
await authStore.getUser()

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}

const route = useRoute()

const getTrending = async (): Promise<XweetsResponse | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get(`/api/hashtags/${route.query.tag}`)
            if (data) {
                return data
            }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getTrending()) || { data: [] }
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
        <Sep title="Topic:" :subtitle="`${$route.query.tag}`" is-sticky />
        <Xweet v-for="xweet in data"
            :key="xweet.xweet_id"
            :id="xweet.xweet_id"
            :userId="xweet.user_id"
            :fullname="xweet.full_name" 
            :username="xweet.username" 
            :body="xweet.body" 
            :media="xweet.media"
            :profilePic="xweet.profile_pic" 
            :createdAt="xweet.created_at" 
            :updated-at="xweet.updated_at" 
            :is-rexweet="false"
            :is-reply="false"
            :is-own="xweet.user_id === authStore.getSignedInUserId" 
            :rexweeted="false"
            :liked="false" />
        <template #sidebarRight>
            <Suggestions v-if="authStore.getIsAuthenticated" />
            <Trending />
        </template>
    </Layout>
</template>