<script setup lang="ts">
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';
import { XweetResponse } from '../../types/xweets';
import { FollowResponse } from '../../types/follows'

const authStore = useAuth()

const getXweets = async (): Promise<XweetResponse | undefined> => {
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
</script>

<template>
    <section 
        class="flex-[4] flex flex-col justify-evenly items-center border border-solid border-sky-800 rounded-xl">
        <div 
            class="flex justify-center items-center gap-4 w-full px-8 pb-4 border-b border-solid border-sky-600/20">
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
            class="flex justify-center items-center gap-2 w-full pb-4 text-sky-800 text-lg border-b border-solid border-sky-600/20 dark:text-white">
            <span class="font-bold">{{ xweetData.length }}</span>
            <span>Zweets</span>
        </div>
        <div 
            class="flex flex-col items-center w-full pb-4 text-sky-800 text-lg border-b border-solid border-sky-600/20 dark:text-white">
            <span><strong>{{ followData[0].data.length }}</strong> Followings</span>
            <span><strong>{{ followData[1].data.length }}</strong> Followers</span>
        </div>
        <div>
            <input type="button" value="New Zweet" class="px-4 py-2 bg-sky-600 text-white text-lg font-bold rounded-xl">
        </div>
    </section>
</template>