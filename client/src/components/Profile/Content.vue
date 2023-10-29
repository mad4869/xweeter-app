<script lang="ts">
export enum Tabs {
    Xweets = 'xweets',
    Following = 'following',
    Followers = 'followers',
    Likes = 'likes'
}
</script>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Header from './Header.vue';
import Toggle from './Toggle.vue';
import Timeline from './Timeline.vue';
import UserList from './UserList.vue';
import Likes from './Likes.vue';
import ProfileForm from './ProfileForm.vue';
import Popup from '@/components/App/Popup.vue';
import Modal from '@/components/App/Modal.vue';
import useAuthStore from '@/stores/useAuthStore';
import { User } from '@/types/auth';
import { useFetchList, useFetchObject } from '@/composables/useFetch';
import useCount, { Features } from '@/composables/useCount';
import useNotify from '@/composables/useNotify'

const authStore = useAuthStore()

const timelineRef = ref<HTMLElement | null>(null)
const likeRef = ref<HTMLElement | null>(null)
const scrollTimeline = useScroll(timelineRef)
const scrollLike = useScroll(likeRef)

const route = useRoute()
const router = useRouter()

const activeTab = ref(route.query.tab || Tabs.Xweets)
const setActiveTab = (tab: Tabs) => {
    if (tab === Tabs.Xweets) {
        router.push('')
    } else {
        router.push({ query: { tab } })
    }

    router.afterEach(() => {
        activeTab.value = route.query.tab || Tabs.Xweets
    })
}

const profile = await useFetchObject<User>(`/api/users/${route.params.id}`, false)
const profileXweetsCount = await useCount('users', parseInt(route.params.id as string), Features.Xweets)
const profileFollowing = await useFetchList<User>(`/api/users/${route.params.id}/following`, false)
const profileFollowers = await useFetchList<User>(`/api/users/${route.params.id}/followers`, false)
const profileFollowingCount = profileFollowing.list.value?.length
const profileFollowersCount = profileFollowers.list.value?.length

const userFollowing = await useFetchList<User>(`/api/users/${authStore.getSignedInUserId}/following`, true)
const userFollowed = userFollowing.list.value?.some(following => following.user_id === profile.obj.value?.user_id)

const notification = ref({ 
    isNotified: false, 
    category: undefined, 
    msg: '' 
    })

const showNotice = (category: 'success' | 'error', msg: string) => {
    useNotify(notification, category, msg)
}

const showModal = ref(false)
</script>

<template>
    <Header
        :is-own="profile.obj.value?.user_id === authStore.getSignedInUserId"
        :user-id="profile.obj.value?.user_id"
        :fullname="profile.obj.value?.full_name"
        :username="profile.obj.value?.username"
        :bio="profile.obj.value?.bio"
        :profile-pic="profile.obj.value?.profile_pic"
        :header-pic="profile.obj.value?.header_pic"
        :xweets-count="profileXweetsCount"
        :following-count="profileFollowingCount"
        :followers-count="profileFollowersCount"
        :is-followed="userFollowed"
        @show-notice="showNotice"
        @show-edit-profile="showModal = true"
        @set-active-tab="setActiveTab" />
    <Toggle :active-tab="activeTab" @set-active-tab="setActiveTab" />
    <Timeline v-show="activeTab === Tabs.Xweets"
        :y="scrollTimeline.y.value"
        :show-notice="showNotice" />
    <UserList v-show="activeTab === Tabs.Following"
        :data="profileFollowing.list.value ?? []" />
    <UserList v-show="activeTab === Tabs.Followers"
        :data="profileFollowers.list.value ?? []" />
    <Likes v-show="activeTab === Tabs.Likes"
        :y="scrollLike.y.value"
        :show-notice="showNotice" />
    <Modal :show="showModal" @clicked-outside="showModal = false">
        <ProfileForm
            :user-id="profile.obj.value?.user_id"
            :username="profile.obj.value?.username"
            :fullname="profile.obj.value?.full_name"
            :email="profile.obj.value?.email"
            :bio="profile.obj.value?.bio"
            :profile-pic="profile.obj.value?.profile_pic"
            :header-pic="profile.obj.value?.header_pic"
            @close-modal="showModal = false"
            @show-notice="showNotice" />
    </Modal>
    <Popup
        :show="notification.isNotified"
        :category="notification.category" 
        :message="notification.msg" />
</template>