<template>
    <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100">
        <h2 class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3 mb-6">
            Ihre aktuellen Stromdaten
        </h2>

        <Household v-model="data.household" />

        <div class="my-12"/>

        <h2 class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3">
            <span class="text-blue-500 font-mono text-xl"></span>
            Weitere Angaben
        </h2>


        <ModulesPV v-model="data.pv" />
        <ModulesEV v-model="data.ev" class="" />
        <ModulesHeatPump v-model="data.heat_pump" />
        <ModulesBattery v-model="data.battery" />

        <div class="my-16"/>

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