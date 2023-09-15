<script setup lang="ts">
import useAuth from '../../composables/useAuth';

const authStore = useAuth()

const signedInUser = {
    username: authStore.getSignedInUsername
}
</script>

<template>
    <section class="flex-[2] flex flex-col justify-evenly items-center border border-solid border-sky-800 rounded-xl">
        <div class="flex justify-between items-center w-full px-8 pb-4 border-b border-solid border-sky-600/20">
            <div>
                <span
                    class="w-10 h-10 px-3 py-2 bg-white text-xs border border-solid border-sky-800 rounded-full text-center">A</span>
            </div>
            <div class="flex flex-col">
                <span class="text-white font-bold">Budi Sudarsono</span>
                <span class="text-sm text-sky-800">@{{ signedInUser.username }}</span>
            </div>
        </div>
        <div
            class="flex justify-center items-center gap-2 w-full pb-4 text-white text-lg border-b border-solid border-sky-600/20">
            <span class="font-bold">1150</span>
            <span>Zweets</span>
        </div>
        <div class="flex flex-col items-center w-full pb-4 text-white text-lg border-b border-solid border-sky-600/20">
            <span><strong>700</strong> Followings</span>
            <span><strong>650</strong> Followers</span>
        </div>
        <div>
            <input type="button" value="New Zweet" class="px-4 py-2 bg-sky-600 text-white text-lg font-bold rounded-xl">
        </div>
    </section>
</template>