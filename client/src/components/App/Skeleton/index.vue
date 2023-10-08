<script setup lang="ts">
import Layout from '@/components/App/Layout/index.vue'
import Header from './Header.vue'
import Content from './Content.vue';
import Suggestions from './Suggestions.vue';
</script>

<template>
    <Layout>
        <Header />
        <Content />
        <template #sidebarRight>
            <Suggestions />
        </template>
    </Layout>
</template>