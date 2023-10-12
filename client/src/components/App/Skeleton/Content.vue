<template>
    <section class="flex flex-col gap-4">
        <div v-for="_ in 3"
            class="px-4 py-4 flex justify-center items-center gap-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl">
            <div class="flex-1 flex flex-col items-center gap-2 h-full px-4 border-r border-solid border-sky-600/20">
                <div class="w-10 h-10 bg-slate-600 border border-solid border-sky-800 rounded-full animate-pulse"></div>
                <div class="flex flex-col justify-center items-center gap-2 w-full text-center">
                    <div v-for="_ in 2" class="w-full h-4 bg-slate-600 rounded-sm animate-pulse"></div>
                </div>
            </div>
            <div class="flex flex-col justify-center items-center gap-2 w-4/5 h-full">
                <div v-for="_ in 3" class="w-full h-4 bg-slate-600 rounded-sm animate-pulse"></div>
            </div>
        </div>
    </section>
</template>