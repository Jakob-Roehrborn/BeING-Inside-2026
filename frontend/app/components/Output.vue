<template>
    <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100 transition-all duration-300"
        :class="{ 'opacity-60 pointer-events-none': !props.results && !props.isLoading }">
        <h2 class="text-2xl font-semibold text-slate-900 border-b-2 border-slate-100 pb-3 mb-8">
            Ihr geschätztes Ergebnis
        </h2>

        <div v-if="props.isLoading" class="text-center py-16 text-slate-600 space-y-4">
            <svg class="animate-spin h-10 w-10 text-blue-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
            </svg>
            <p class="text-lg">Frage Backend-Daten ab...</p>
        </div>

        <div v-else-if="props.results" class="space-y-10">
            <div class="bg-green-50 border border-green-200 rounded-xl p-6 text-center shadow-inner">
                <h3 class="text-sm font-medium text-green-800 uppercase tracking-wider mb-2">Mögliche Ersparnis pro
                    Jahr*</h3>
                <div class="text-5xl font-extrabold text-green-900 leading-none">
                    {{ props.results.savings }} <span class="text-4xl font-bold">€</span>
                </div>
            </div>

            <div class="space-y-4">
                <h4 class="text-lg font-semibold text-slate-800">Kostenvergleich im Detail</h4>
                <div class="space-y-3">
                    <div
                        class="flex justify-between items-center py-3 px-4 bg-slate-50 rounded-lg border border-slate-100">
                        <span class="text-slate-600">Bisherige Kosten (geschätzt):</span>
                        <span class="font-semibold text-slate-900">{{ props.results.oldCost }} €</span>
                    </div>
                    <div
                        class="flex justify-between items-center py-3 px-4 bg-blue-50 rounded-lg border border-blue-100">
                        <span class="text-blue-900 font-medium">Kosten Dynamischer Tarif:</span>
                        <span class="font-bold text-green-700 text-lg">{{ props.results.newCost }} €</span>
                    </div>
                    <div
                        class="flex justify-between items-center py-3 px-4 bg-slate-50 rounded-lg border border-slate-100 text-sm">
                        <span class="text-slate-600">Effektiver Arbeitspreis neu:</span>
                        <span class="font-medium text-slate-800">{{ props.results.avgNewPrice }} Ct/kWh</span>
                    </div>
                </div>
            </div>

            <div
                class="h-40 bg-slate-50 border-2 border-dashed border-slate-200 flex items-center justify-center my-8 text-slate-400 rounded-xl px-4 text-center text-sm">
                [ Hier könnte ein Balkendiagramm (Alt vs. Neu) eingebunden werden ]
            </div>

            <div
                class="bg-amber-50 border-l-4 border-amber-300 p-4 rounded-r-lg text-amber-900 text-xs leading-relaxed mt-10">
                <p class="font-semibold mb-1">Hinweis zur Berechnung:</p>
                *Dies ist eine unverbindliche Schätzung basierend auf Ihrem angegebenen Jahresverbrauch und Ihrem
                Flexibilitätsprofil. Die Berechnung nutzt historische Day-Ahead-Börsenstrompreise (Spotmarkt) des
                vergangenen Jahres inkl. anfallender Steuern, Abgaben und Netzentgelte. Die tatsächliche Ersparnis hängt
                stark von Ihrem realen Verbrauchsverhalten ab.
            </div>
        </div>

        <div v-else
            class="text-center py-20 px-6 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 text-slate-500 space-y-4">
            <svg class="w-16 h-16 mx-auto text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                    d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 002-2H7a2 2 0 00-2 2v14a2 2 0 002 2z">
                </path>
            </svg>
            <p class="text-lg">Bitte füllen Sie die Daten auf der linken Seite aus und klicken Sie auf
                <strong>"Berechnen"</strong>, um Ihr Ergebnis zu sehen.</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type outputData from '~/types/outputData';

const props = defineProps<{
    isLoading: boolean,
    results: outputData,
}>()


</script>

<style>

</style>