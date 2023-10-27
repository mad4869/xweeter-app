<script setup lang="ts">
import { TopDailyUser } from '@/types/users'

defineProps<{
    data: TopDailyUser[] | undefined
    totalData: number | undefined
}>()
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
                    <td>{{ index + 1 }}</td>
                    <td class="hover:text-sky-600" :title="`View @${user.username}'s profile'`">
                        <router-link :to="`/users/${user.user_id}`">@{{ user.username }}</router-link>
                    </td>
                    <td>{{ user.xweet_count }}</td>
                </tr>
            </tbody>
        </table>
        <p>
            Showing {{ (totalData as number) > 0 ? 1 : 0 }} {{ (totalData as number) > 1 ? `- ${totalData}` : '' }} of 
            {{ totalData }} {{ totalData === 1 ? 'entry' : 'entries' }}
        </p>
    </section>
</template>

<style scoped>
.h-table {
    min-height: calc(100vh - 20rem);
}
</style>