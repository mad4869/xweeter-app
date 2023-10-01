<script setup lang="ts">
import UserToFollow from './UserToFollow.vue';
import useAuth from '../../composables/useAuth';
import { sendReqCookie } from '../../utils/axiosInstances';
import { FollowResponse, WhoToFollowResponse } from '../../types/follows';

const authStore = useAuth()

const getActiveUsers = async (): Promise<WhoToFollowResponse | undefined> => {
    try {
        const { data } = await sendReqCookie.get('/api/users/most-active')
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const getFollow = async (): Promise<FollowResponse | undefined> => {
    try {
        const following = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/following`)
        const followers = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/followers`)
        if (following.data && followers.data) {
            return {
                following: following.data, 
                followers: followers.data
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getActiveUsers()) || { data: [] }
const followData = await getFollow()
const userNotFollowed = data.filter(user => {
    return !followData?.following.data.some(followed => followed.user_id === user.user_id)
})
</script>

<template>
    <section 
        class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Who to Follow</span>
            <font-awesome-icon icon="fa-regular fa-user" class="text-white" />
        </div>
        <div class="flex flex-col justify-center gap-2 overflow-scroll">
            <UserToFollow
                v-for="user in userNotFollowed" 
                :key="user.user_id"
                :id="user.user_id" 
                :fullname="user.full_name" 
                :username="user.username"
                :last-xweet="user.body"
                :profile-pic="user.profile_pic" />
        </div>
    </section>
</template>