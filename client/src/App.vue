<script setup lang="ts">
import Skeleton from '@/components/App/Skeleton/index.vue'
</script>

<template>
  <Suspense>
    <router-view></router-view>
    <template #fallback>
      <Skeleton />
    </template>
  </Suspense>
</template>
