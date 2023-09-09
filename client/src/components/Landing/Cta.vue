<script setup lang="ts">
import Toggle from './Toggle.vue';
import SignupForm from './SignupForm.vue';
</script>

<template>
    <section
        class="col-start-2 flex flex-col justify-center items-center gap-4 px-4 py-4 bg-white/10 backdrop-blur-lg rounded-lg shadow-md shadow-sky-800">
        <Toggle />
        <SignupForm />
    </section>
</template>

<style scoped></style>