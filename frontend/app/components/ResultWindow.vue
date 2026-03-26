<template>
    <div class="flex flex-col justify-between items-center py-3 px-4 bg-slate-50 rounded-lg border border-slate-100 gap-2">
        <span class="text-slate-500">{{ title }}</span>
        <span class="font-semibold text-slate-900">{{ `${value.toFixed(2)} ${unit}` }}</span>
    </div>
</template>

<script lang="ts" setup>
const props = defineProps<{
    title: string,
    value: number,
    unit: string,
}>()
</script>