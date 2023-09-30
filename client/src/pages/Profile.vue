<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRoute } from 'vue-router';

import Layout from '../components/App/Layout/index.vue'
import Popup from '../components/App/Popup.vue';
import Setting from '../components/App/Setting.vue';
import Header from '../components/Profile/Header.vue';
import Profile from '../components/Home/Profile.vue';
import Timeline from '../components/Profile/Timeline.vue';
import useAuth from '../composables/useAuth';
import { sendReqCookie } from '../utils/axiosInstances';
import { Users } from '../types/auth';
import Modal from '../components/App/Modal.vue';
import ProfileForm from '../components/Profile/ProfileForm.vue';

const authStore = useAuth()
await authStore.getUser()

const route = useRoute()

const notification = reactive({
    isNotified: false,
    notifMsg: '',
    category: ''
})

const getUser = async () => {
    try {
        const { data } = await sendReqCookie.get<{ data: Users, success: boolean } | undefined>(`/api/users/${route.params.id}`)
        if (data) {
            return data
        }
    } catch (err) {
        console.error(err)
    }
}

const { data } = (await getUser()) || { data: undefined }

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
            <Setting />
        </template>
        <Header
            :is-own="data?.user_id === authStore.getSignedInUserId"
            :user-id="data?.user_id"
            :fullname="data?.full_name"
            :username="data?.username"
            :bio="data?.bio"
            :profile-pic="data?.profile_pic"
            :header-pic="data?.header_pic"
            @change-profile-pic="handleProfilePic"
            @show-edit-profile="showModal" />
        <Timeline />
        <Modal :show="isModalShown" @clicked-outside="handleClickOutsideModal">
            <ProfileForm
                :username="data?.username"
                :fullname="data?.full_name"
                :bio="data?.bio"
                :profile-pic="data?.profile_pic"
                :header-pic="data?.header_pic" />
        </Modal>
        <Popup
            :show="notification.isNotified"
            category="success" 
            :message="notification.notifMsg" 
            />
    </Layout>
</template>
