<template>
    <div class="flex flex-col gap-1.5">
        <label v-if="label" :for="id" class="text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ label }}
            <span v-if="required" class="text-red-500">*</span>
        </label>

        <div class="relative">
            <input :id="id" type="time" :value="modelValue" :disabled="disabled" :required="required"
                @input="$emit('update:modelValue', $event.target.value)"
                class="block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:focus:border-blue-400 dark:focus:ring-blue-400" />

            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                <svg class="h-4 w-4 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
        </div>

        <p v-if="hint" class="text-xs text-gray-500 dark:text-gray-400">
            {{ hint }}
        </p>
    </div>
</template>

<script setup>
import { computed } from 'vue'

// Define props
const props = defineProps({
    modelValue: {
        type: String,
        default: '',
        // Native time input expects "HH:mm" format (24h) under the hood
    },
    label: {
        type: String,
        default: ''
    },
    hint: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    },
    required: {
        type: Boolean,
        default: false
    }
})

// Define emits for v-model compatibility
defineEmits(['update:modelValue'])

// Generate a unique ID for accessibility linking between label and input
const id = computed(() => `time-input-${Math.random().toString(36).substring(2, 9)}`)
</script>

<style scoped>
/* Hides the native clock icon in webkit browsers 
  so our custom SVG icon doesn't overlap it.
*/
input[type="time"]::-webkit-calendar-picker-indicator {
    display: none;
    -webkit-appearance: none;
}
</style>