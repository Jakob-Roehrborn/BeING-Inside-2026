<template>
    <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100">
        <div class="flex flex-row justify-between border-b-2 border-slate-100 pb-3 mb-6 items-end">
            <h2 class="text-2xl font-semibold text-slate-900 w-2/3">
                Ihre aktuellen Stromdaten
            </h2>
            <div class="flex flex-row justify-end w-1/3 text-sm">
                <span class="text-red-500 ml-1 font-bold">*</span>
                <span class="pl-1">Pflichtfeld</span>
            </div>
        </div>

        <Household v-model="data.household" />

        <div class="my-12" />

        <h2 class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3">
            <span class="text-blue-500 font-mono text-xl"></span>
            Weitere Angaben
        </h2>


        <ModulesPV v-model="data.pv" />
        <ModulesEV v-model="data.ev" />
        <ModulesHeatPump v-model="data.heat_pump" />
        <ModulesBattery v-model="data.battery" />

        <div class="my-16" />

        <UtilsSubmitButton @submit="submit" :is-loading="isLoading" />
    </div>
</template>

<script lang="ts" setup>

import type inputData from '~/types/inputData';

const props = defineProps<{
    isLoading: boolean,
}>()

const emit = defineEmits(['submit'])

const data = defineModel<inputData>({ required: true })

function submit() {
    emit("submit")
}

</script>

<style></style>