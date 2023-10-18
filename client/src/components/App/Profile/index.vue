<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'
import { sendReqCookie } from '@/utils/axiosInstances';
import { FollowDetailResponse, FollowResponse } from '@/types/follows'
import { XweetsResponse } from '@/types/xweets';

const emit = defineEmits<{
    (e: 'show-new-xweet'): void
}>()

const authStore = useAuthStore()

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
countStore.xweetsCount = data.length

const getFollow = async (): Promise<FollowDetailResponse | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const following = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/following`)
            const followers = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/followers`)
            if (following.data && followers.data) {
                return {
                    following: following.data, 
                    followers: followers.data
                }
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const { following, followers } = await getFollow() || { following: [], followers: [] }
</script>

<template>
    <section 
        class="flex-[4] grid grid-rows-4 border border-solid border-sky-800 rounded-xl">
        <router-link
            :to="`/users/${authStore.getSignedInUserId}`" 
            class="flex items-center justify-center w-full row-start-1 gap-4 border-b border-solid border-sky-600/20">
            <div>
                <img 
                    :src="authStore.getSignedInPfp" 
                    class="object-cover w-12 h-12 border border-solid rounded-full border-sky-800" />
            </div>
            <div class="flex flex-col text-sky-600">
                <span class="font-bold">
                    {{ authStore.getSignedInFullname }}
                </span>
                <span class="text-sm">
                    @{{ authStore.getSignedInUsername }}
                </span>
            </div>
        </router-link>
        <div
            class="flex flex-col items-center justify-center w-full row-start-2 gap-1 text-lg border-b border-solid text-sky-800 border-sky-600/20 dark:text-white">
            <strong class="text-3xl">{{ countStore.xweetsCount }}</strong>
            <span class="text-white/50">Xweets</span>
        </div>
        <div 
            class="flex flex-col items-center justify-center w-full row-start-3 text-lg border-b border-solid text-sky-800 border-sky-600/20 dark:text-white">
            <div class="flex items-center justify-center w-full gap-2">
                <strong class="flex-1 text-right">{{ (following as FollowResponse).data.length }}</strong>
                <span class="flex-[2] text-white/50">Following</span>
            </div>
            <div class="flex items-center justify-center w-full gap-2">
                <strong class="flex-1 text-right">{{ (followers as FollowResponse).data.length }}</strong>
                <span class="flex-[2] text-white/50">
                    {{ (followers as FollowResponse).data.length === 1 ? 'Follower' : 'Followers' }}
                </span>
            </div>
        </div>
        <div class="flex items-center justify-center row-start-4">
            <button  
                title="Add New Xweet"
                class="flex items-center gap-2 px-4 py-2 text-lg font-bold text-white transition-colors cursor-pointer bg-sky-600 rounded-xl hover:bg-sky-800"
                @click="$emit('show-new-xweet')">
                <font-awesome-icon icon="fa-solid fa-feather" />
                <span>New Xweet</span>
            </button>
        </div>
    </section>
</template>