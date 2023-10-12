<template>
    <section class="flex-1 flex flex-col gap-4 border border-solid border-sky-800 rounded-xl overflow-hidden">
        <div class="flex justify-between items-center px-4 py-2 bg-sky-600">
            <span class="text-white font-semibold">Who to Follow</span>
            <font-awesome-icon icon="fa-regular fa-user" class="text-white" />
        </div>
        <div v-for="_ in 2" class="flex flex-col justify-center gap-2 overflow-scroll">
            <section class="flex flex-col items-center gap-2 px-8 py-1">
                <div class="grid grid-cols-4 grid-rows-2 gap-y-1 w-full">
                    <div class="col-start-1 col-span-1 row-start-1 row-span-2 flex items-center">
                        <div alt="Profile Pic"
                            class="w-8 h-8 bg-slate-600 border border-solid border-sky-800 rounded-full animate-pulse">
                        </div>
                    </div>
                    <div class="col-start-2 col-span-3 row-start-1 row-span-1 bg-slate-600 rounded-sm animate-pulse"></div>
                    <div class="col-start-2 col-span-3 row-start-2 row-span-1 bg-slate-600 rounded-sm animate-pulse"></div>
                </div>
                <div class="w-full h-8 bg-slate-600 rounded-sm animate-pulse">
                </div>
            </section>
        </div>
    </section>
</template>