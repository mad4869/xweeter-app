<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRoute } from 'vue-router';

import Layout from '@/components/App/Layout/index.vue'
import Popup from '@/components/App/Popup.vue';
import Settings from '@/components/App/Settings/index.vue';
import Modal from '@/components/App/Modal.vue';
import Profile from '@/components/App/Profile/index.vue';
import Header from '@/components/Profile/Header.vue';
import ProfileForm from '@/components/Profile/ProfileForm.vue';
import Timeline from '@/components/Profile/Timeline.vue';
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie, sendReqWoCookie } from '@/utils/axiosInstances';
import { User } from '@/types/auth';
import { FollowResponse } from '@/types/follows';

type Response = {
    data: {
        xweet_id: number,
        user_id: number,
        username: string,
        full_name: string,
        body: string,
        profile_pic: string,
        created_at: string,
        rexweet_id: number,
        og_username: string,
        og_full_name: string,
        og_profile_pic: string
    }[],
    success: boolean
}

const authStore = useAuthStore()
await authStore.getUser()

const route = useRoute()

const notification = reactive({
    isNotified: false,
    notifMsg: '',
    category: ''
})

const getUser = async () => {
    try {
        const { data } = await sendReqWoCookie.get<{ data: User, success: boolean } | undefined>(
            `/api/users/${route.params.id}`
        )
        if (data) {
            console.log(data)
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const user = (await getUser()) || { data: undefined }

const getProfileTimeline = async (): Promise<Response | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get(`api/users/${route.params.id}/profile-timeline`)
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const timeline = (await getProfileTimeline()) || { data: [] }

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

const followData = await getFollow()
const userFollowed = followData?.following.data.some(following => following.user_id === user.data?.user_id)

const handleProfilePic = (
    isSuccess: boolean,
    isError: boolean,
    notifMsg: string
) => {
    notification.isNotified = true
    notification.notifMsg = notifMsg

    if (isSuccess) {
        notification.category = 'success'

        setTimeout(() => {
            notification.isNotified = false
        }, 3000)
    } else if (isError) {
        notification.category = 'error'
    }
}

const isModalShown = ref(false)
const showModal = () => {
    isModalShown.value = true
}
const handleClickOutsideModal = () => {
    isModalShown.value = false
}
</script>

<template>
    <Layout>
        <template #sidebarLeft>
            <!-- <section 
                v-if="!authStore.getIsAuthenticated"
                class="flex-[4] flex flex-col items-center px-2 pt-4 border border-solid border-sky-800 rounded-xl">
                <Toggle :active-btn="activeBtn" @activate-btn="activateBtn" />
                <Transition name="fade" mode="out-in">
                    <KeepAlive>
                        <SignupForm :use-title="false" v-if="activeBtn === UserAuth.SignUp" />
                        <SigninForm :use-title="false" v-else />
                    </KeepAlive>
                </Transition>
            </section> -->
            <Profile v-if="authStore.getIsAuthenticated" />
            <Settings />
        </template>
        <Header
            :is-own="user.data?.user_id === authStore.getSignedInUserId"
            :user-id="user.data?.user_id"
            :fullname="user.data?.full_name"
            :username="user.data?.username"
            :bio="user.data?.bio"
            :profile-pic="user.data?.profile_pic"
            :header-pic="user.data?.header_pic"
            :xweets-count="timeline.data.length"
            :following-count="0"
            :followers-count="0"
            :is-followed="userFollowed"
            @change-profile-pic="handleProfilePic"
            @show-edit-profile="showModal" />
        <Timeline 
            :is-own="parseInt($route.params.id as string) === authStore.getSignedInUserId"
            :data="timeline.data" />
        <Modal :show="isModalShown" @clicked-outside="handleClickOutsideModal">
            <ProfileForm
                :user-id="user.data?.user_id"
                :username="user.data?.username"
                :fullname="user.data?.full_name"
                :email="user.data?.email"
                :bio="user.data?.bio"
                :profile-pic="user.data?.profile_pic"
                :header-pic="user.data?.header_pic" />
        </Modal>
        <Popup
            :show="notification.isNotified"
            category="success" 
            :message="notification.notifMsg" 
            />
    </Layout>
</template>
