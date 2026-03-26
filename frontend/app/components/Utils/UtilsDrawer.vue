<template>
    <div class="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-sm transition-all duration-300">
        <!-- Header / Toggle Button -->
        <button @click="isOpen = !isOpen"
            class="w-full flex items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 transition-colors focus:outline-none"
            :aria-expanded="isOpen">
            <span class="font-semibold text-slate-800">{{ title }}</span>

            <!-- Chevron Icon -->
            <svg class="w-5 h-5 text-slate-500 transform transition-transform duration-300"
                :class="{ 'rotate-180': isOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        </button>

        <!-- Expandable Content Area -->
        <div class="grid transition-[grid-template-rows] duration-300 ease-in-out"
            :class="isOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'">
            <div class="overflow-hidden">
                <div class="p-4 border-t border-slate-200 bg-white">
                    <!-- The slot allows you to put any content inside the drawer from the parent -->
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

defineProps<{
    title: string
}>()

const isOpen = ref(false)
</script>