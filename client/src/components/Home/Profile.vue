<script setup lang="ts">
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';
import { XweetsResponse } from '../../types/xweets';
import { FollowResponse } from '../../types/follows'

const emit = defineEmits<{
    (e: 'show-new-xweet'): void
}>()

const authStore = useAuth()

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

const getFollow = async (): Promise<FollowResponse[] | undefined> => {
    try {
        if (authStore.getIsAuthenticated) {
            const following = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/following`)
            const followers = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/followers`)
            if (following.data && followers.data) {
                return [following.data, followers.data]
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getXweets()) || { data: [] }
const xweetData = data
const followData = (await getFollow()) || []

const showNewXweet = () => {
    emit('show-new-xweet')
}
</script>

<template>
    <section 
        class="flex-[4] grid grid-rows-4 border border-solid border-sky-800 rounded-xl">
        <div 
            class="row-start-1 flex justify-center items-center gap-4 w-full border-b border-solid border-sky-600/20">
            <div>
                <img :src="authStore.getSignedInPfp" class="w-12 h-12 border border-solid border-sky-800 rounded-full" />
            </div>
            <div class="flex flex-col">
                <span class="text-sky-800 font-bold">
                    {{ authStore.getSignedInFullname }}
                </span>
                <span class="text-sm text-sky-800">
                    @{{ authStore.getSignedInUsername }}
                </span>
            </div>
        </div>
        <div
            class="row-start-2 flex flex-col justify-center items-center gap-1 w-full text-sky-800 text-lg border-b border-solid border-sky-600/20 dark:text-white">
            <strong class="text-3xl">{{ xweetData.length }}</strong>
            <span>Xweets</span>
        </div>
        <div 
            class="row-start-3 flex flex-col justify-center items-center w-full text-sky-800 text-lg border-b border-solid border-sky-600/20 dark:text-white">
            <div class="flex justify-center items-center gap-2 w-full">
                <strong class="flex-1 text-right">{{ followData[0].data.length }}</strong>
                <span class="flex-[2]">Following</span>
            </div>
            <div class="flex justify-center items-center gap-2 w-full">
                <strong class="flex-1 text-right">{{ followData[1].data.length }}</strong>
                <span class="flex-[2]">{{ followData[1].data.length === 1 ? 'Follower' : 'Followers' }}</span>
            </div>
        </div>
        <div class="row-start-4 flex justify-center items-center">
            <button  
                title="Add New Xweet"
                class="flex items-center gap-2 px-4 py-2 bg-sky-600 text-white text-lg font-bold rounded-xl transition-colors cursor-pointer hover:bg-sky-800"
                @click.prevent="showNewXweet">
                <font-awesome-icon icon="fa-solid fa-feather" />
                <span>New Xweet</span>
            </button>
        </div>
    </section>
</template>