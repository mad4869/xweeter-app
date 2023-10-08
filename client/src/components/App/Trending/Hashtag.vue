<script setup lang="ts">
defineProps<{
    body: string,
}>()
</script>

<template>
    <div class="flex flex-col items-center gap-1 px-4 py-1">
        <div class="w-full text-sm text-sky-800 font-bold dark:text-sky-600">
            {{ body }}
        </div>
        <div class="w-full text-xs text-slate-600 dark:text-slate-400">
            261 xweets in the last hour
        </div>
    </div>
</template>