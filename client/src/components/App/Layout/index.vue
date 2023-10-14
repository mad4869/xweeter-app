<script setup lang="ts">
import { ref } from 'vue';

import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
import Modal from '@/components/App/Modal.vue';
import router from '@/routes';
import useAuthStore from '@/stores/useAuthStore';

defineProps({
    showSidebar: {
        type: Boolean,
        default: true
    }
})

const authStore = useAuthStore()

const isError = ref(false)
const isLoading = ref(false)
const showModal = ref(false)

const signout = async () => {
    isLoading.value = true

    await authStore.signout()

    isLoading.value = false

    if (!authStore.getIsAuthenticated) {
        router.push('/')
    } else {
        isError.value = true
        setTimeout(() => {
            isError.value = false
        }, 3000)
    }
}
</script>

<template>
    <Navbar @show-signout-modal="() => { showModal = true }" />
    <main class="grid w-full grid-cols-5 px-4 py-4 gap-x-4">
        <aside
            v-if="showSidebar" 
            class="sticky flex flex-col justify-center col-span-1 gap-4 top-20 h-side">
            <slot name="sidebarLeft"></slot>
        </aside>
        <article 
            class="flex flex-col gap-4" 
            :class="showSidebar ? 'col-span-3' : 'col-span-5'">
            <slot></slot>
        </article>
        <aside
            v-if="showSidebar" 
            class="sticky flex flex-col justify-center col-span-1 gap-4 top-20 h-side">
            <slot name="sidebarRight"></slot>
        </aside>
    </main>
    <Modal :show="showModal" @clicked-outside="() => { showModal = false }">
        <section class="w-[50vw] h-36 flex flex-col items-center gap-4 text-white">
            <div class="w-full py-2 font-semibold text-center bg-red-600/60">
                <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
                <p>{{ isLoading ? '' : isError ? 'Failed to sign out. Please try again.' : 'Sign Out' }}</p>
            </div>
            <p>Are you sure you want to sign out?</p>
            <div class="flex items-center justify-center gap-4">
                <button 
                    class="w-10 py-1 rounded-md bg-red-600/60 hover:bg-red-600 active:shadow-inner" 
                    title="Confirm sign out" 
                    @click="signout">
                    Yes
                </button>
                <button 
                    class="w-10 py-1 border border-solid rounded-md border-red-600/60 hover:border-red-600" 
                    title="Cancel"
                    @click="() => { showModal = false }">
                    No
                </button>
            </div>
        </section>
    </Modal>
    <Footer />
</template>

<style scoped>
.h-side {
    height: calc(100vh - 6rem);
}
</style>
