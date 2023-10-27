<script setup lang="ts">
import Empty from '@/components/App/Empty.vue';
import { User } from '@/types/auth'

defineProps<{
    data: User[]
}>()
</script>

<template>
    <section class="flex flex-col gap-4">
        <div v-for="user in data" 
            :key="user.user_id"
            class="flex items-center gap-4 p-4 border border-solid bg-sky-600/10 backdrop-blur-lg border-sky-800 rounded-xl">
            <div>
                <img 
                    :src="user.profile_pic" 
                    alt="Profile Pic"
                    class="object-cover w-12 h-12 border border-solid rounded-full border-sky-800" 
                    loading="lazy">
            </div>
            <div class="flex flex-col flex-1 gap-2">
                <p class="flex items-center gap-2 text-sky-600">
                    <span class="font-semibold">{{ user.full_name }}</span>
                    <span class="text-sm">@{{ user.username }}</span>
                </p>
                <p class="text-xs text-white">{{ user.bio }}</p>
            </div>
        </div>
        <Empty v-if="data.length === 0" msg="There are no users yet" />
    </section>
</template>