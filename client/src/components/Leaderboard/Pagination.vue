<script setup lang="ts">
import { ref } from 'vue';

const {pages} = defineProps<{
    pages: number
}>()

const activePage = ref(1)

const changePage = (page: number) => {
    activePage.value = page
}
const nextPage = () => {
    if (activePage.value < pages) {
        activePage.value++
    }
}
const prevPage = () => {
    if (activePage.value > 1) {
        activePage.value--
    }
}
</script>

<template>
    <section class="flex justify-between items-center px-2 py-2 bg-sky-800/20 backdrop-blur-sm">
        <font-awesome-icon 
            icon="fa-regular fa-square-caret-left" 
            class="text-sky-800 cursor-pointer"
            @click.prevent="prevPage" />
        <div class="flex items-center gap-1">
            <div 
                v-for="page in pages"
                class="px-2 text-white cursor-pointer"
                :class="page === activePage ? 'bg-sky-800 rounded' : ''"
                @click.prevent="changePage(page)">
                {{ page }}
            </div>
        </div>
        <font-awesome-icon 
            icon="fa-regular fa-square-caret-right" 
            class="text-sky-800 cursor-pointer"
            @click.prevent="nextPage" />
    </section>
</template>