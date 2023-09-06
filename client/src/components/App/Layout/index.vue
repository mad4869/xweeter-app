<script setup lang="ts">
import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
</script>

<template>
    <Navbar />
    <slot></slot>
    <Footer />
</template>

<style scoped></style>
