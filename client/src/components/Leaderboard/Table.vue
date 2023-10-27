<script setup lang="ts">
import { watch } from 'vue';

import { TopDailyUser } from '@/types/users'

const props = defineProps<{
    data: TopDailyUser[] | undefined
    dataLength: number | undefined
    dataTotal: number | undefined
    page: number
    entries: number
}>()

let initialIndex = 0
let lastIndex = 0

watch(() => [props.page, props.entries, props.dataLength], () => {
    initialIndex = props.page === 1 ? 1 : props.entries + 1
    lastIndex = (props.dataLength as number) >= props.entries ? 
                (props.dataLength as number) * props.page : 
                props.dataTotal ?? 0
}, {
    immediate: true
})

</script>

<template>
    <section class="dark:text-sky-600 h-table">
        <table class="table-auto w-full border-separate text-sky-800 text-center dark:text-white">
            <thead class="bg-sky-800">
                <tr>
                    <th>No.</th>
                    <th>Users</th>
                    <th>Xweets Count</th>
                </tr>
            </thead>
            <tbody class="bg-sky-800/30">
                <tr v-for="(user, index) in data">
                    <td>{{ page === 1 ? index + 1 : index + 1 + entries }}</td>
                    <td class="hover:text-sky-600" :title="`View @${user.username}'s profile'`">
                        <router-link :to="`/users/${user.user_id}`">@{{ user.username }}</router-link>
                    </td>
                    <td>{{ user.xweet_count }}</td>
                </tr>
            </tbody>
        </table>
        <p>
            Showing {{ initialIndex }} {{ initialIndex < lastIndex ? `- ${lastIndex}` : '' }} of 
            {{ dataTotal }} {{ dataTotal === 1 ? 'entry' : 'entries' }}
        </p>
    </section>
</template>

<style scoped>
.h-table {
    min-height: calc(100vh - 20rem);
}
</style>