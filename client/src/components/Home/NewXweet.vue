<script setup lang="ts">
import { computed, ref } from 'vue';

const MAX_CHARS = 140
const chars = ref('')
const charCount = computed(() => chars.value.length)
</script>

<template>
    <section 
        class="px-12 flex flex-col justify-between items-center border border-solid border-sky-800 rounded-xl">
        <span class="w-full py-4 text-2xl text-sky-950 dark:text-white">New Xweet</span>
        <textarea 
            name="new-tweet" 
            id="new-tweet" 
            placeholder="Tell them what have you been up to..." 
            spellcheck="false"
            v-model="chars"
            class="w-full h-10 px-4 py-2 bg-sky-200 rounded-lg caret-sky-800 resize-none transition-[height] duration-300 ease-out placeholder:text-sky-400 focus:h-32 focus:outline-none dark:bg-slate-200 dark:placeholder:text-slate-400"
            :class="charCount > MAX_CHARS ? 'text-red-600 focus-visible:outline-red-600' : 'text-slate-700 focus-visible:outline-sky-600'">
        </textarea>
        <div class="w-full py-4 flex justify-between items-start">
            <label for="add-image" title="Add image to your xweet">
                <span 
                    class="px-2 py-1 bg-slate-800/50 text-xs text-white rounded-md cursor-pointer hover:bg-slate-800 dark:bg-slate-400/50 dark:hover:bg-slate-400">
                    Add Image
                </span>
                <input 
                    type="file" 
                    id="add-image" 
                    alt="Add Image" 
                    accept="image/jpeg, image/png" 
                    multiple class="hidden">
            </label>
            <div 
                class="text-red-400 transition-opacity duration-200" 
                :class="charCount > MAX_CHARS ? 'opacity-100' : 'opacity-0'">
                Your xweet exceeds the maximum number of characters
            </div>
            <input 
                type="submit" 
                value="Xweet"
                class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer disabled:bg-slate-200 disabled:cursor-not-allowed"
                :disabled="charCount > MAX_CHARS">
        </div>
    </section>
</template>