<template>
    <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100 transition-all duration-300"
        :class="{ 'opacity-60 pointer-events-none': !results && !isLoading }">

        <h2 class="text-2xl font-semibold text-slate-900 border-b-2 border-slate-100 pb-3 mb-8">
            Ihr geschätztes Ergebnis
        </h2>

        <!-- laden -->
        <div v-if="isLoading" class="text-center py-16 text-slate-600 space-y-4">
            <svg class="animate-spin h-10 w-10 text-blue-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
            </svg>
            <p class="text-lg">Frage Backend-Daten ab...</p>
        </div>

        <div v-else-if="results" class="flex flex-col justify-around gap-4">

            <h4 class="text-lg font-semibold text-slate-800">Preisinformationen</h4>
            <div class="flex flex-row gap-8">
                <div class="flex flex-col gap-4 w-1/2">
                    <ResultWindow title="Kosten normaler Tarif" :value="results.cost_const" unit="€" />
                    <ResultWindow title="Kosten dynamischer Tarif" :value="results.cost_dynamic" unit="€" />
                </div>

                <!-- <ResultWindow title="Ersparte Kosten mit dem dynamischen Tarif" :value="results.savings_dynamic" unit="€" class="bg-green-50! text-3xl!"/> -->
                <div
                    class="flex flex-col w-1/2 border justify-between rounded-xl p-4 text-center shadow-inner"
                    :class="results.savings_dynamic > 0 ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'">
                    <h3 class="text-sm font-medium text-green-800 uppercase">
                        Insgesamt erspart
                    </h3>
                    <div class="text-lg md:text-5xl font-extrabold leading-none" :class="results.savings_dynamic > 0 ? 'text-green-900' : 'text-red-900'">
                        {{ results.savings_dynamic.toFixed(2) }} €
                    </div>
                    <h3 class="text-sm font-medium uppercase" :class="results.savings_dynamic > 0 ? 'text-green-900' : 'text-red-900'" >
                        mit dem dynamischen Tarif
                    </h3>
                </div>

            </div>

            <div class="my-3" />

            <!-- Sektion: Jährlicher Energieverbrauch -->
            <h4 class="text-lg font-semibold text-slate-800">Jährliche Energiebilanz</h4>

            <div class="flex flex-col gap-4">
                <ResultWindow title="Insgesamt ins Netz eingespeist" :value="results.netz_einspeisung_kwh" unit="kWh"
                    class="bg-green-50!  border-green-100!" />
                <ResultWindow title="Insgesamt aus dem Netz bezogen" :value="results.netz_bezug_kwh" unit="kWh"
                    class="bg-red-50!  border-red-100!" />
            </div>

            <div class="flex flex-col gap-4 bg-slate-50 rounded-xl p-4 border-2 border-dashed border-slate-200">
                <h4 class="font-semibold text-slate-800 w-full text-center">Zusammensetzung:</h4>
                <ResultWindow title="PV-Anlage" :value="results.solar" unit="kWh"
                    class="bg-green-50!  border-green-100!" />
                <div class="flex flex-row justify-between gap-4">
                    <ResultWindow title="Haushalt" :value="results.household" unit="kWh"
                        class="bg-red-50! border-red-100! w-1/3" />
                    <ResultWindow title="Wärmepumpe" :value="results.heat_pump" unit="kWh"
                        class="bg-red-50!  border-red-100! w-1/3" />
                    <ResultWindow title="Elektroauto" :value="results.ecar" unit="kWh"
                        class="bg-red-50!  border-red-100! w-1/3" />
                </div>
            </div>

            <div class="mt-2">
                <ResultWindow title="Insgesamt steuerbarer Verbrauch" :value="results.controllable_load" unit="kWh"
                    class="border-indigo-400! border-2 " />
            </div>

            <!-- doesnt work on prod -->
            <!-- <UtilsDrawer title="Detailierte Diagramme" >
                <div class="flex flex-col gap-4">
                    <span class="font-semibold bg-slate-200 rounded-lg" @click="open_diagram(0)">Kumulierte Kostenbilanz übers Jahr</span>
                    <span class="font-semibold bg-slate-200 rounded-lg" @click="open_diagram(1)">Netzeinspeisung und Netzbezug übers Jahr</span>
                    <span class="font-semibold bg-slate-200 rounded-lg" @click="open_diagram(2)">Netzeinspeisung und Netzbezug übers Jahr (kumuliert)</span>
                </div>
            </UtilsDrawer>
            <div class="my-3" /> -->

            <!-- Sektion: EnWG Modul -->
            <div class="space-y-4">
                <h4 class="text-lg font-semibold text-slate-800">Kosten nach Modulen §14a EnWG</h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <ResultWindow title="Modul 1" :value="results.cost_modul_1" unit="€" class="outline-2"
                        :class="results.guenstig_m == 1 ? 'bg-green-50! outline-green-100' : 'outline-red-50 bg-red-50!'" />
                    <ResultWindow title="Modul 2" :value="results.cost_modul_2" unit="€" class="outline-2"
                        :class="results.guenstig_m == 2 ? 'bg-green-50! outline-green-100' : 'outline-red-50 bg-red-50!'" />
                    <ResultWindow title="Modul 3" :value="results.cost_modul_3" unit="€" class="outline-2"
                        :class="results.guenstig_m == 3 ? 'bg-green-50! outline-green-100' : 'outline-red-50 bg-red-50!'" />
                </div>
                <ResultWindow class="w-full bg-green-50! outline-green-100" title="Ersparnis durch Auswahl des besten Moduls" unit="€" :value="results.ersparnis"/>
            </div>

        </div>


        <!-- Leerer Zustand -->
        <div v-else
            class="text-center py-20 px-6 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 text-slate-500 space-y-4">
            <svg class="w-16 h-16 mx-auto text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                    d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 002-2H7a2 2 0 00-2 2v14a2 2 0 002 2z">
                </path>
            </svg>
            <p class="text-lg">Bitte füllen Sie die Daten auf der linken Seite aus und klicken Sie auf
                <strong>"Berechnen"</strong>, um Ihr Ergebnis zu sehen.
            </p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type outputData from '~/types/outputData';
import ResultWindow from './ResultWindow.vue';
import UtilsDrawer from './Utils/UtilsDrawer.vue';

const module_list = computed(() => {
    return [props.results!.cost_modul_1, props.results!.cost_modul_2, props.results!.cost_modul_3]
})

const best_module = computed(() => {
    return module_list.value.indexOf(Math.max(...module_list.value));
})

const props = defineProps<{
    isLoading: boolean,
    results: outputData | undefined,
}>()

function open_diagram(n: number) {
    const DIAGRAMS = ["cost_diagram.html", "plot_grid_exchange.html", "plot_grid_exchange_cumsum.html"]
    window.open(`http://localhost:5000/api/diagrams/${DIAGRAMS[n]}`, '_blank');
}

</script>