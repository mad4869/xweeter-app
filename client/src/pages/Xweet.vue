<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';

import Layout from '../components/App/Layout/index.vue'
import Toggle from '@/components/App/Auth/Toggle.vue';
import SigninForm from '@/components/App/Auth/SigninForm.vue';
import SignupForm from '@/components/App/Auth/SignupForm.vue';
import Setting from '@/components/App/Settings/index.vue';
import Suggestions from '@/components/App/Suggestions/index.vue';
import Trending from '@/components/App/Trending/index.vue';
import Xweet from '@/components/App/Xweet/index.vue';
import Profile from '@/components/App/Profile/index.vue';
import Sep from '@/components/App/Sep.vue';
import useAuthStore from '@/stores/useAuthStore';
import { UserAuth } from '@/types/auth';
import { XweetResponse } from '@/types/xweets';
import { RepliesResponse } from '@/types/replies'
import { sendReqWoCookie } from '@/utils/axiosInstances';

const authStore = useAuthStore()
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
        <Sep title="Xweet from:" :subtitle="`@${xweet.data?.username}`" :is-sticky="false" />
        <div class="flex flex-col">
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
                :is-reply="false"
                :is-own="xweet.data?.user_id === authStore.getSignedInUserId" 
                :rexweeted="false"
                :liked="false" />
            <Sep v-if="data.length > 0" title="Replies" is-sticky />
            <div class="flex flex-col gap-2">
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
                    :is-reply="true"
                    :is-own="reply.user_id === authStore.getSignedInUserId" 
                    :rexweeted="false"
                    :liked="false" />
            </div>
        </div>
        <template #sidebarRight>
            <Suggestions v-if="authStore.getIsAuthenticated" />
            <Trending />
        </template>
    </Layout>
</template>