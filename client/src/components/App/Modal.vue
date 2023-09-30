<script setup lang="ts">
import { ref } from 'vue';
import { TransitionRoot } from '@headlessui/vue';
import { onClickOutside } from '@vueuse/core/index.mjs';

defineProps<{
    show: boolean
}>()

const emit = defineEmits<{
    (e: 'clicked-outside'): void
}>()

const modalRef = ref<HTMLDivElement | null>(null)

onClickOutside(modalRef, () => {
    emit('clicked-outside')
})
</script>

<template>
    <TransitionRoot
        :show="show"
        as="dialog"
        class="fixed left-0 right-0 top-0 bottom-0 w-screen h-screen flex justify-center items-center bg-black/60 backdrop-blur-md z-30"
        enter="transition-transform ease-out"
        enter-from="scale-0"
        enter-to="scale-100"
        leave="transition-transform ease-in"
        leave-from="scale-100"
        leave-to="scale-0">
        <section
            ref="modalRef"
            class="flex justify-center items-center max-w-[75%] max-h-[75%] border border-solid border-white rounded-lg">
            <slot></slot>
        </section>
    </TransitionRoot>
</template>