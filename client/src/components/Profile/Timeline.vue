<script setup lang="ts">
import Xweet from '@/components/App/Xweet/index.vue';
import Empty from '@/components/App/Empty.vue';

defineProps<{
    isOwn: boolean,
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
    }[]
}>()
</script>

<template>
    <section class="flex flex-col gap-4">
        <Xweet 
            v-for="xweet in data" 
            :key="xweet.xweet_id" 
            :id="xweet.xweet_id"
            :userId="xweet.user_id"
            :fullname="xweet.full_name" 
            :username="xweet.username"
            :body="xweet.body" 
            :profilePic="xweet.profile_pic" 
            :createdAt="xweet.created_at"
            :isRexweet="xweet.rexweet_id !== undefined"
            :isReply="false" 
            :og_username="xweet.og_username" 
            :og_fullname="xweet.og_full_name"
            :og_profile_pic="xweet.og_profile_pic"
            :isOwn="true"
            :rexweeted="false"
            :liked="false" />
        <div v-if="data.length === 0">
            <Empty
                v-if="isOwn"
                msg="You haven't xweet anything yet"
                submsg="Start telling your stories now!" />
            <Empty
                v-else
                msg="This user hasn't xweet anything yet" />
        </div>
    </section>
</template>