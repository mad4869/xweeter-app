<template>
    <section class="flex-[4] grid grid-rows-4 border border-solid border-sky-800 rounded-xl">
        <div class="row-start-1 flex justify-center items-center gap-4 w-full border-b border-solid border-sky-600/20">
            <div class="w-12 h-12 bg-slate-600 border border-solid border-sky-800 rounded-full animate-pulse"></div>
            <div class="flex flex-col justify-center items-center gap-2 h-full">
                <div v-for="_ in 2" class="w-24 h-4 bg-slate-600 rounded-sm animate-pulse"></div>
            </div>
        </div>
        <div
            class="row-start-2 flex flex-col justify-center items-center gap-1 w-full border-b border-solid border-sky-600/20">
            <div v-for="_ in 2" class="w-24 h-4 bg-slate-600 rounded-sm animate-pulse"></div>
        </div>
        <div
            class="row-start-3 flex flex-col justify-center items-center gap-1 w-full border-b border-solid border-sky-600/20">
            <div v-for="_ in 2" class="w-24 h-4 bg-slate-600 rounded-sm animate-pulse"></div>
        </div>
        <div class="row-start-4 flex justify-center items-center">
            <div class="w-36 h-8 bg-slate-600 rounded-sm animate-pulse"></div>
        </div>
    </section>
</template>