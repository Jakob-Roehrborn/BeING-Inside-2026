<template>
    <div>
        <label for="consumption" class="text-sm font-medium text-slate-700 mb-1 pl-1.5">
            {{ props.title }}
        </label>
        <div class="relative rounded-md shadow-sm">
            <input type="number" v-model.number="model" :placeholder="props.placeholder ? `z.B. ${props.placeholder}` : ''"
                class="w-full px-4 py-3 text-lg styled-input" />
            <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                {{ props.unit }}
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>

const props = defineProps<{
    title: String,
    placeholder?: String,
    unit?: String,
    disabled?: boolean,
}>()

const model = defineModel()

</script>

<style></style>