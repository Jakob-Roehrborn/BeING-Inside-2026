<template>
    <div class="flex flex-col gap-1.5">
        <label v-if="label" class="text-sm font-medium text-slate-700 mb-1 pl-1.5 inline-flex items-center">
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1 font-bold">*</span>
        </label>

        <div>
            <input v-model="timeStr" type="time" :disabled="disabled" :required="required"
                class="w-full styled-input px-4 py-2" />
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

<script setup lang="ts">

const props = defineProps < {
    label: string
    hint?: string,
    disabled?: boolean,
    required?: boolean,

} > ()

const model = defineModel < number > ({ required: true })

const timeStr = ref()

watch(timeStr, (timeStr) => {
    if (!timeStr) return null

    const [hours, minutes] = timeStr.split(':').map(Number)

    model.value = Math.round((hours + (minutes / 60)) * 100) / 100
    console.log(model.value)
})

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