<script setup lang="ts">
defineProps<{
    users: string,
    xweetsCount: number
}>()
</script>

<template>
    <table class="table-auto border-separate text-white text-center">
        <thead class="bg-slate-700">
            <tr>
                <th>Users</th>
                <th>Xweets Count</th>
            </tr>
        </thead>
        <tbody class="bg-slate-800">
            <tr>
                <td>{{ users }}</td>
                <td>{{ xweetsCount }}</td>
            </tr>
        </tbody>
    </table>
</template>