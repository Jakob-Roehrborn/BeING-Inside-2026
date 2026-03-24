<template>
    <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100">
        <div class="space-y-10">

            <Household v-model="data.household"/>

            <div>
                <h2
                    class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3">
                    <span class="text-blue-500 font-mono text-xl"></span>
                    Weitere Angaben
                </h2>
                

                <ModulesPV v-model="data.pv"/>
                <ModulesEV v-model="data.ev" class=""/>
                <ModulesBattery v-model="data.battery"/>
                <ModulesHeatPump v-model="data.heat_pump"/>
               
                <!-- <div class="space-y-3 mb-8">
                    <label
                        class="flex items-center gap-4 p-4 border rounded-xl border-slate-200 hover:bg-slate-50 cursor-pointer transition">
                        <input type="checkbox" v-model="formData.hasEV"
                            class="h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                        <span class="text-base text-slate-800">Ich besitze ein <strong>Elektroauto</strong></span>
                    </label>
                    <label
                        class="flex items-center gap-4 p-4 border rounded-xl border-slate-200 hover:bg-slate-50 cursor-pointer transition">
                        <input type="checkbox" v-model="formData.hasHeatPump"
                            class="h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                        <span class="text-base text-slate-800">Ich nutze eine <strong>Wärmepumpe</strong></span>
                    </label>
                    <label
                        class="flex items-center gap-4 p-4 border rounded-xl border-slate-200 hover:bg-slate-50 cursor-pointer transition">
                        <input type="checkbox" v-model="data.battery"
                            class="h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                        <span class="text-base text-slate-800">Ich habe einen <strong>Batteriespeicher</strong></span>
                    </label>
                </div>

                <div class="form-group bg-slate-50 p-6 rounded-xl border border-slate-100">
                    <label for="shiftable"
                        class="block text-base font-semibold text-slate-800 mb-3 flex justify-between items-center">
                        Verschiebbarer Jahresverbrauch
                        <span class="text-3xl font-bold text-blue-600">{{ formData.shiftablePercentage }}%</span>
                    </label>
                    <input type="range" id="shiftable" v-model="formData.shiftablePercentage" min="0" max="100"
                        class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600" />
                    <p class="mt-3 text-sm text-slate-600 leading-relaxed">
                        Schätzen Sie, wie viel Prozent Ihres Gesamtverbrauchs Sie gezielt in günstige Zeiten (z.B.
                        Nachts, Mittags bei Sonne) verlegen können (Laden, Heizen, Waschen).
                    </p>
                </div> -->
            </div>

            <button
                class="w-full flex justify-center items-center gap-2 py-4 px-6 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-60 disabled:cursor-not-allowed text-lg"
                @click="submit" :disabled="props.isLoading">
                <svg v-if="props.isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg"
                    fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                </svg>
                {{ props.isLoading ? 'Berechnung läuft...' : 'Einsparpotenzial berechnen' }}
            </button>
        </div>
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

<style>

</style>