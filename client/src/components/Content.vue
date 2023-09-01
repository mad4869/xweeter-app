<script setup lang="ts">
import NewZweet from './NewZweet.vue';
import Zweet from './Zweet.vue';
import Sep from './Sep.vue';
import Profile from './Profile.vue';

const contents = [
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
    { fullname: 'Budi Sudarsono', username: '@BudiSudarsono', zweet: 'I have been better lately' },
]
</script>

<template>
    <main class="grid grid-cols-5 gap-x-4 w-full px-4 py-4">
        <aside class="sticky top-20 col-span-1 h-[50vh]">
            <Profile />
        </aside>
        <article class="col-span-3 flex flex-col gap-4">
            <NewZweet />
            <Sep title="Timeline" />
            <Zweet v-for="(content, index) in contents" :key="index" :fullname="content.fullname"
                :username="content.username" :zweet="content.zweet" />
        </article>
        <aside class="col-span-1"></aside>
    </main>
</template>

<style scoped></style>