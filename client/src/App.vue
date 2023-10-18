<template>
  <Suspense>
    <router-view :key="$route.fullPath"></router-view>
  </Suspense>
</template>
