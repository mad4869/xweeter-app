<script setup lang="ts">
import { TopDailyUser } from '../../types/users'

defineProps<{
    data: TopDailyUser[],
}>()
</script>

<template>
    <table class="table-auto border-separate text-sky-800 text-center dark:text-white">
        <thead class="bg-slate-700">
            <tr>
                <th>Users</th>
                <th>Xweets Count</th>
            </tr>
        </thead>
        <tbody class="bg-slate-800">
            <tr v-for="user in data">
                <td class="hover:bg-slate-700" :title="`View @${user.username}'s profile'`">
                    <router-link :to="`/users/${user.user_id}`">@{{ user.username }}</router-link>
                </td>
                <td>{{ user.xweet_count }}</td>
            </tr>
        </tbody>
    </table>
</template>