<template>
    <div>
        <label for="consumption" class="text-sm font-medium text-slate-700 mb-1 pl-1.5 inline-flex items-center">
            {{ props.title }}
            <span v-if="props.required" class="text-red-500 ml-1 font-bold">*</span>
        </label>

        <div class="relative rounded-md shadow-sm">
            <input type="number" v-model.number="model"
                :placeholder="props.placeholder ? `z.B. ${props.placeholder}` : ''" :disabled="props.disabled"
                :required="props.required" class="w-full px-4 py-3 text-lg styled-input"
                :class="{ 'opacity-50 cursor-not-allowed': props.disabled }" />

            <div v-if="props.unit"
                class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                {{ props.unit }}
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
const props = defineProps<{
    title: string,
    placeholder?: string,
    unit?: string,
    disabled?: boolean,
    required?: boolean,
}>()

const model = defineModel()
</script>