<script setup lang="ts">
// const MAX_CHARS = 140
</script>

<template>
    <section class="px-12 flex flex-col justify-between items-center border border-solid border-sky-800 rounded-xl">
        <span class="w-full py-4 text-2xl text-white">New Zweet</span>
        <textarea name="new-tweet" id="new-tweet" placeholder="Tell them what have you been up to..." spellcheck="false"
            class="w-full h-10 px-4 py-2 bg-slate-200 text-slate-700 rounded-lg caret-sky-800 resize-none transition-[height] duration-300 ease-out placeholder:text-slate-400 focus:h-32 focus:outline-none focus-visible:outline-sky-600"></textarea>
        <div class="w-full py-4 flex justify-between items-start">
            <label for="add-image">
                <span class="px-2 py-1 bg-slate-400/50 text-xs text-white rounded-md cursor-pointer hover:bg-slate-400">Add
                    Image
                </span>
                <input type="file" id="add-image" alt="Add Image" accept="image/jpeg, image/png" multiple class="hidden">
            </label>
            <input type="submit" value="Zweet"
                class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md cursor-pointer">
        </div>
    </section>
</template>