<template>
    <section class="flex flex-col gap-4">
        <div
            v-for="div in 3"
            :key="div"
            class="px-4 py-4 flex justify-center items-center gap-4 bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl">
            <div class="bg-slate-600 rounded-sm animate-pulse"></div>
        </div>
    </section>
</template>