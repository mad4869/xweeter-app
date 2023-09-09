<script setup lang="ts">
import { ref } from 'vue'
import { useVueTable, getCoreRowModel, createColumnHelper, FlexRender } from '@tanstack/vue-table'

type User = {
    username: string,
    zweetCount: number
}

const defaultData: User[] = [
    {
        username: '@BudiSudarsono',
        zweetCount: 100
    },
    {
        username: '@Kazusa',
        zweetCount: 50
    }
]

const columnHelper = createColumnHelper()

const columns = [
    columnHelper.group({
        header: 'Leaderboard',
        columns: [
            columnHelper.accessor(() => 'no', {
                header: 'No'
            }),
            columnHelper.accessor(() => 'username', {
                header: 'Username'
            }),
            columnHelper.accessor(() => 'zweet-count', {
                header: 'Zweets'
            })
        ]
    })
]

const data = ref(defaultData)

const table = useVueTable({
    data: data.value,
    columns,
    getCoreRowModel: getCoreRowModel()
})
</script>

<template>
    <table>
        <thead>
            <tr v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
                <th v-for="header in headerGroup.headers" :key="header.id" :colSpan="header.colSpan">
                    <FlexRender v-if="!header.isPlaceholder" :render="header.column.columnDef.header" />
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="row in table.getRowModel().rows" :key="row.id">
                <td v-for="cell in row.getVisibleCells()" :key="cell.id">
                    <FlexRender :render="cell.column.columnDef.cell" />
                </td>
            </tr>
        </tbody>
    </table>
</template>