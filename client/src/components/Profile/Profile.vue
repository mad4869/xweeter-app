<script setup lang="ts">
import Zweet from '../../components/App/Zweet.vue';

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
    <section class="flex flex-col gap-4">
        <Zweet v-for="(content, index) in contents" :key="index" :fullname="content.fullname" :username="content.username"
            :zweet="content.zweet" />
    </section>
</template>

<style scoped></style>