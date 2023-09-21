<template>
  <Suspense>
    <router-view></router-view>
    <template #fallback>
      <h1 class="text-white">Loading...</h1>
    </template>
  </Suspense>
</template>
