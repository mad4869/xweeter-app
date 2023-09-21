<script setup lang="ts">
defineProps<{
    body: string,
}>()
</script>

<template>
    <div class="flex flex-col items-center gap-1 px-4 py-1">
        <div class="w-full text-sm text-sky-600 font-bold">
            {{ body }}
        </div>
        <div class="w-full text-xs text-slate-400">
            261 xweets in the last hour
        </div>
    </div>
</template>