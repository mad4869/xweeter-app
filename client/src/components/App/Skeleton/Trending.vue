<template>
    <section class="flex-1 flex flex-col gap-3 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Trending</span>
        </div>
        <div v-for="_ in 3" class="flex flex-col gap-2 w-3/4 mx-auto">
            <div class="w-full h-8 bg-slate-600 rounded-sm animate-pulse"></div>
            <div class="w-full h-4 bg-slate-600 rounded-sm animate-pulse"></div>
        </div>
    </section>
</template>