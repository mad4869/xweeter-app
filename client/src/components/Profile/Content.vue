<script lang="ts">
export enum Tabs {
    Xweets = 'xweets',
    Following = 'following',
    Followers = 'followers',
    Likes = 'likes'
}
</script>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Header from './Header.vue';
import Toggle from './Toggle.vue';
import Timeline from './Timeline.vue';
import UserList from './UserList.vue';
import LikeList from './LikeList.vue';
import ProfileForm from './ProfileForm.vue';
import Popup from '@/components/App/Popup.vue';
import Modal from '@/components/App/Modal.vue';
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie, sendReqWoCookie } from '@/utils/axiosInstances';
import { UserResponse } from '@/types/users';
import { FollowResponse, FollowDetailResponse } from '@/types/follows';
import { XweetsResponse } from '@/types/xweets';

const authStore = useAuthStore()

const route = useRoute()

const timelineRef = ref<HTMLElement | null>(null)
const likeRef = ref<HTMLElement | null>(null)
const scrollTimeline = useScroll(timelineRef)
const scrollLike = useScroll(likeRef)

const activeTab = ref(Tabs.Xweets)

const getProfile = async () => {
    try {
        const { data } = await sendReqWoCookie.get<UserResponse | undefined>(
            `/api/users/${route.params.id}`
        )
        if (data?.success) {
            return data.data
        }
    } catch (err) {
        console.error(err)
    }
}

const profile = await getProfile()

const getProfileXweets = async () => {
    try {
        const { data } = await sendReqWoCookie.get<XweetsResponse | undefined>(
            `/api/users/${route.params.id}/xweets`
        )
        if (data?.success) {
            return data.data
        }
    } catch (err) {
        console.error(err)
    }
}

const xweets = await getProfileXweets() || []

const getSignedUserFollowing = async (): Promise<FollowResponse | undefined> => {
    try {
        const { data } = await sendReqCookie.get(`/api/users/${authStore.getSignedInUserId}/following`)
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const userFollowingData = await getSignedUserFollowing()
const userFollowed = userFollowingData?.data.some(following => following.user_id === profile?.user_id)

const getProfileFollowingFollowers = async (): Promise<FollowDetailResponse | undefined> => {
    try {
        const followingData = await sendReqCookie.get(`/api/users/${route.params.id}/following`)
        const followersData = await sendReqCookie.get(`/api/users/${route.params.id}/followers`)
        if (followingData && followersData) {
            return {
                following: followingData.data,
                followers: followersData.data
            }
        }
    } catch (err) {
        console.error(err)
    }
}

const { following, followers } = await getProfileFollowingFollowers() || { following: [], followers: [] }

const notification = reactive<{
    isNotified: boolean,
    category?: 'success' | 'error'
    msg: string
}>({
    isNotified: false,
    msg: ''
})

const showNotice = (category: 'success' | 'error', msg: string) => {
    notification.isNotified = true
    notification.category = category
    notification.msg = msg

    setTimeout(() => {
        notification.isNotified = false
        notification.msg = ''
    }, 3000)
}

const handleProfilePic = (
    isSuccess: boolean,
    isError: boolean,
    notifMsg: string
) => {
    notification.isNotified = true
    notification.msg = notifMsg

    if (isSuccess) {
        notification.category = 'success'

        setTimeout(() => {
            notification.isNotified = false
        }, 3000)
    } else if (isError) {
        notification.category = 'error'
    }
}

const showModal = ref(false)
</script>

<template>
    <Header
        :is-own="profile?.user_id === authStore.getSignedInUserId"
        :user-id="profile?.user_id"
        :fullname="profile?.full_name"
        :username="profile?.username"
        :bio="profile?.bio"
        :profile-pic="profile?.profile_pic"
        :header-pic="profile?.header_pic"
        :xweets-count="xweets.length"
        :following-count="(following as FollowResponse).data.length"
        :followers-count="(followers as FollowResponse).data.length"
        :is-followed="userFollowed"
        @change-profile-pic="handleProfilePic"
        @show-edit-profile="() => { showModal = true }" />
    <Toggle :active-tab="activeTab" @set-active-tab="tab => { activeTab = tab }" />
    <Timeline v-show="activeTab === Tabs.Xweets"
        :y="scrollTimeline.y.value"
        :show-notice="showNotice"
        @show-notice="showNotice" />
    <UserList v-show="activeTab === Tabs.Following"
        :data="(following as FollowResponse).data" />
    <UserList v-show="activeTab === Tabs.Followers"
        :data="(followers as FollowResponse).data" />
    <LikeList v-show="activeTab === Tabs.Likes"
        :y="scrollLike.y.value"
        :show-notice="showNotice"
        @show-notice="showNotice" />
    <Modal :show="showModal" @clicked-outside="() => { showModal = false }">
        <ProfileForm
            :user-id="profile?.user_id"
            :username="profile?.username"
            :fullname="profile?.full_name"
            :email="profile?.email"
            :bio="profile?.bio"
            :profile-pic="profile?.profile_pic"
            :header-pic="profile?.header_pic" />
    </Modal>
    <Popup
        :show="notification.isNotified"
        :category="notification.category" 
        :message="notification.msg" 
        />
</template>