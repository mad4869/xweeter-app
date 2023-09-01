<script setup lang="ts">
import Navbar from './components/Navbar.vue';
import NewZweet from './components/NewZweet.vue';
import Zweet from './components/Zweet.vue';
import Sep from './components/Sep.vue';

const contents = [
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
  { username: '@BudiSudarsono', zweet: 'I have been better lately' },
]
</script>

<template>
  <Navbar />
  <NewZweet />
  <Sep title="Timeline" />
  <Zweet v-for="(content, index) in contents" :key="index" :username="content.username" :zweet="content.zweet" />
</template>

<style scoped></style>
