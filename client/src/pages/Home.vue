<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue';
import { useWindowScroll } from '@vueuse/core';

import Layout from '../components/App/Layout/index.vue'
import Settings from '@/components/App/Settings/index.vue';
import Suggestions from '@/components/App/Suggestions/index.vue';
import Xweets from '@/components/App/Xweet/index.vue';
import Modal from '@/components/App/Modal.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import Profile from '@/components/App/Profile/index.vue';
import Sep from '@/components/App/Sep.vue';
import SigninForm from '@/components/App/Auth/SigninForm.vue';
import SignupForm from '@/components/App/Auth/SignupForm.vue';
import Toggle from '@/components/App/Auth/Toggle.vue';
import Trending from '@/components/App/Trending/index.vue';
import Popup from '@/components/App/Popup.vue'
// import MoreXweet from '@/components/App/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import useAuthStore from '@/stores/useAuthStore';
import { UserAuth } from '@/types/auth';
import { Xweet, XweetsResponse } from '@/types/xweets';
import { LikesFullResponse } from '@/types/likes'
import { UpdateTimeline } from '@/types/timeline';
import socket from '@/utils/socket';
import { sendReqCookie, sendReqWoCookie } from '@/utils/axiosInstances';

const authStore = useAuthStore()
await authStore.getUser()

const start = ref(0)

const getTimeline = async (): Promise<XweetsResponse | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(
                `/api/users/${authStore.getSignedInUserId}/timeline?start=${start.value}`
            )
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

const getXweets = async (): Promise<XweetsResponse | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const { data } = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/xweets`)
            if (data) {
                return data
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getXweets()) || { data: [] }
const xweetCount = ref(data.length)

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
const timeline = reactive<Xweet[]>(initialTimeline)
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

const { y } = useWindowScroll()
const isLoading = ref(false)
const moreXweet = ref<HTMLElement | null>(null)
const needsMoreXweet = ref(true)
const threshold = ref<number | undefined>(0)
onMounted(() => {
    const moreXweetRect = moreXweet.value?.getBoundingClientRect()
    threshold.value = (moreXweetRect?.top || 0)
})

watch(y, async (newY, oldY) => {
    console.log(newY, oldY)
    if (newY >= (threshold.value ?? 0) && newY !== oldY) {
        isLoading.value = true
        start.value+= 10
        
        try {
            const { data } = (await getTimeline()) || { data: [] }
            if (data.length > 0) {
                timeline.push(...data)
            } else {
                needsMoreXweet.value = false
            }
        } catch (err) {
            console.error('Error fetching timeline data:', err);
        } finally {
            isLoading.value = false;
        }
    }
})

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
                <Transition mode="out-in">
                    <KeepAlive>
                        <SignupForm :use-title="false" v-if="activeBtn === UserAuth.SignUp" />
                        <SigninForm :use-title="false" v-else />
                    </KeepAlive>
                </Transition>
            </section>
            <Profile 
                v-if="authStore.getIsAuthenticated"
                :xweet-count="xweetCount"
                @show-new-xweet="showModal" />
            <Settings />
        </template>
        <NewXweet v-if="authStore.getIsAuthenticated" @increment-xweet-count="() => { xweetCount++ }" />
        <Sep title="Timeline" is-sticky />
        <div v-for="xweet in timeline" class="flex flex-col gap-4">
            <Xweets
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
                :liked="likes.includes(xweet.xweet_id)"
                @update-timeline="updateTimeline"
                @show-notice="showNotice"
                @reply="showReplyEditor" />
            <ReplyXweet 
                :show="replyingToXweetId === xweet.xweet_id"
                :xweet-id="xweet.xweet_id"
                @close-reply="() => { replyingToXweetId = null }" />
        </div>
        <section ref="moreXweet" class="flex justify-center items-center">
            <div class="w-1/2 py-2 bg-sky-800 text-sky-400 text-center rounded-full">
                <font-awesome-icon 
                    v-if="isLoading"
                    icon="fa-solid fa-circle-notch" spin />
                {{ !isLoading ? 'More Xweets' : '' }}
            </div>
        </section>
        <Empty 
            v-if="timeline.length === 0"
            msg="This is where your timeline would appear" 
            submsg="Start following some people to get contents to your desire!" />
        <Modal :show="isModalShown" @clicked-outside="handleClickOutsideModal">
            <NewXweet in-modal 
                @increment-xweet-count="() => { xweetCount++ }"
                @close-modal="() => { isModalShown = false }" />
        </Modal>
        <Popup 
            :show="notification.isNotified" 
            message="Success!" 
            :category="notification.category" />
        <template #sidebarRight>
            <Suggestions />
            <Trending />
        </template>
    </Layout>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
    @apply transition-all duration-300 ease-out
}

.v-enter-from,
.v-leave-to {
    @apply translate-x-4 opacity-0
}
</style>