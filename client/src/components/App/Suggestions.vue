<script setup lang="ts">
import User from './User.vue';

const users = [
    { fullname: 'Kazusa Okuyama', username: '@kazusa', lastXweet: 'Let\'s go!' },
    { fullname: 'Tsukasa Senpai', username: '@tsukasa', lastXweet: 'Ikuyo!' },
]
</script>

<template>
    <section 
        class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Who to Follow</span>
            <font-awesome-icon icon="fa-regular fa-user" class="text-white" />
        </div>
        <div class="flex flex-col justify-center gap-2 overflow-scroll">
            <User 
                v-for="(user, index) in users" 
                :key="index" 
                :fullname="user.fullname" 
                :username="user.username"
                :last-xweet="user.lastXweet" />
        </div>
    </section>
</template>