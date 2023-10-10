<script setup lang="ts">
defineProps<{
    inputName: 'new-xweet' | 'modal-new-xweet' | 'edit-xweet' | 'reply-xweet'
    modelValue?: string | string[] | number
    charCount: number
    maxCharCount: number
}>()
</script>

<template>
    <textarea  
        :name="inputName"
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)" 
        placeholder="What's on your mind..." 
        spellcheck="false"
        :autofocus="inputName === 'modal-new-xweet' || inputName === 'edit-xweet'"
        class="w-full h-10 px-4 py-2 bg-sky-200 rounded-lg caret-sky-800 resize-none transition-[height] duration-300 ease-out placeholder:text-sky-400 focus:h-32 focus:outline-none dark:bg-slate-200 dark:placeholder:text-slate-400"
        :class="charCount > maxCharCount ? 'text-red-600 focus-visible:outline-red-600' : 'text-slate-700 focus-visible:outline-sky-600'">
    </textarea>
</template>