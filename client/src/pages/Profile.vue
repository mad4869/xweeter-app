<script setup lang="ts">
import { reactive } from 'vue';

import Layout from '../components/App/Layout/index.vue'
import Popup from '../components/App/Popup.vue';
import Header from '../components/Profile/Header.vue';
import Profile from '../components/Profile/Profile.vue';
import useAuth from '../composables/useAuth';

const authStore = useAuth()
await authStore.getUser()

const notification = reactive({
    isNotified: false,
    notifMsg: '',
    category: ''
})

const handleProfilePic = (
    isSuccess: boolean,
    isError: boolean,
    notifMsg: string
) => {
    notification.isNotified = true
    notification.notifMsg = notifMsg

    if (isSuccess) {
        notification.category = 'success'
    } else if (isError) {
        notification.category = 'error'
    }
}
</script>

<template>
    <Layout>
        <Header @change-profile-pic="handleProfilePic" />
        <Profile />
        <Popup
            v-if="notification.isNotified"
            category="success" 
            message="Ashiappp" 
            />
    </Layout>
</template>
