<script setup lang="ts">
import { ref, reactive } from 'vue';

import Layout from '../components/App/Layout/index.vue'
import Setting from '../components/App/Setting.vue';
import Suggestions from '../components/App/Suggestions.vue';
import SuggestionsLoading from '../components/App/SuggestionsLoading.vue';
import Xweet from '../components/App/Xweet.vue';
import Modal from '../components/App/Modal.vue';
import NewXweet from '../components/Home/NewXweet.vue';
import Profile from '../components/Home/Profile.vue';
import Sep from '../components/Home/Sep.vue';
import SigninForm from '../components/App/SigninForm.vue';
import SignupForm from '../components/App/SignupForm.vue';
import Toggle from '../components/App/Toggle.vue';
import Trending from '../components/App/Trending.vue';
import Popup from '../components/App/Popup.vue'
import useAuth from '../composables/useAuth';
import { UserAuth } from '../types/auth';
import { Xweets, XweetsResponse } from '../types/xweets';
import { LikesFullResponse } from '../types/likes'
import { UpdateTimeline } from '../types/timeline';
import socket from '../utils/socket';
import { sendReqCookie, sendReqWoCookie } from '../utils/axiosInstances';
import Empty from '../components/App/Empty.vue';

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

const getLikes = async (): Promise<LikesFullResponse | undefined> => {
    try {
        if (!authStore.getIsAuthenticated) {
            return
        }

        const { data } = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/likes`)
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const timelineData = (await getTimeline()) || { data: [] }
const initialTimeline = [...timelineData.data]
const timeline = reactive<Xweets[]>(initialTimeline)
socket.on('add_to_timeline', (xweet) => {
    timeline.unshift(xweet)
})
const updateTimeline = (event: UpdateTimeline, xweet_id?: number) => {
    if (event === UpdateTimeline.Delete) {
        const index = timeline.findIndex(xweet => xweet.xweet_id === xweet_id)
        if (index !== -1) {
            timeline.splice(index, 1)
        }
    }

    if (event === UpdateTimeline.Restore) {
        timeline.length = 0
        timeline.push(...initialTimeline)
    }
}

const likes = reactive<number[]>([])
const likesData = (await getLikes()) || { data: [] }
likesData.data.forEach(like => {
    likes.push(like.xweet_id)
})

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}

const notification = reactive<{
    isNotified: boolean,
    category: 'success' | 'error' | undefined
}>({
    isNotified: false,
    category: undefined
})

const showNotice = (category: 'success' | 'error') => {
    console.log(category)
    notification.isNotified = true
    notification.category = category

    setTimeout(() => {
        notification.isNotified = false
        notification.category = undefined
    }, 3000)
}

const isModalShown = ref(false)
const showModal = () => {
    isModalShown.value = true
}
const handleClickOutsideModal = () => {
    isModalShown.value = false
}

const replyingToXweetId = ref<number | null>(null)
const showReplyEditor = (xweet_id: number | null) => {
    replyingToXweetId.value = xweet_id
}
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
            <Profile 
                v-if="authStore.getIsAuthenticated"
                @show-new-xweet="showModal" />
            <Setting />
        </template>
        <NewXweet v-if="authStore.getIsAuthenticated" />
        <Sep title="Timeline" />
        <div v-for="xweet in timeline" class="flex flex-col gap-4">
            <Xweet 
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
                :is-own="xweet.user_id === authStore.getSignedInUserId" 
                :rexweeted="false"
                :liked="likes.includes(xweet.xweet_id)"
                @update-timeline="updateTimeline"
                @show-notice="showNotice"
                @reply="showReplyEditor" />
            <NewXweet is-reply 
                v-if="replyingToXweetId === xweet.xweet_id"
                :xweet-id="xweet.xweet_id" />
        </div>
        <Empty 
            v-if="timeline.length === 0"
            msg="This is where your timeline would appear" 
            submsg="Start following some people to get contents to your desire!" />
        <Modal :show="isModalShown" @clicked-outside="handleClickOutsideModal">
            <NewXweet />
        </Modal>
        <Popup 
            :show="notification.isNotified" 
            message="Success!" 
            :category="notification.category" />
        <template #sidebarRight>
            <Suspense v-if="authStore.getIsAuthenticated">
                <Suggestions />
                <template #fallback>
                    <SuggestionsLoading />
                </template>
            </Suspense>
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