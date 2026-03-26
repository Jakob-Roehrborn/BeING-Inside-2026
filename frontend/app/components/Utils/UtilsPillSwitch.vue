<template>
    <button type="button" role="switch" :aria-checked="model" @click="model = !model"
        class="group relative h-6 w-12 flex-none cursor-pointer rounded-full transition-colors duration-150 ease-in-out shadow-[inset_1px_1px_1px_rgba(0,0,0,0.08)] hover:shadow-[inset_1px_1px_2px_rgba(0,0,0,0.12)]"
        :class="model ? 'bg-sachsenrot' : 'bg-slate-300'">
        <span
            class="absolute top-0.5 left-0.5 block h-5 w-5 rounded-full bg-white transition-transform duration-150 ease-in-out will-change-transform shadow-[1px_1px_1px_rgba(0,0,0,0.08)] group-hover:shadow-[1px_1px_1px_rgba(0,0,0,0.12)] bg-[radial-gradient(circle_at_6px_6px,transparent_0,rgba(0,0,0,0.05)_16px)] group-hover:bg-[radial-gradient(circle_at_6px_6px,transparent_0,rgba(0,0,0,0.0375)_16px)]"
            :class="model ? 'translate-x-6' : 'translate-x-0'"></span>
    </button>
</template>

<script setup lang="ts">
const model = defineModel<boolean>({ required: true })
</script>