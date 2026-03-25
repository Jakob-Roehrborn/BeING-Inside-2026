<template>
    <div class="min-h-screen bg-slate-50 text-slate-900 antialiased py-10 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">

            <header class="text-center mb-12">
                <Header />
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">

                <InputForm v-model="inData!" :is-loading="isLoading" @submit="calculateSavings" />

                <Output :is-loading="isLoading" , :results="outData!" />

            </div>

        </div>
    </div>
</template>

<script lang="ts" setup>
import type inputData from './types/inputData';
import { defaultData } from './types/inputData';
import type outputData from './types/outputData';


// // State für UI
const isLoading = ref(false);
const results = ref(null);

const inData = ref<inputData>({
    household: {

    },
    battery: {
        present: false
    },
    ev: {
        present: false
    },
    pv: {
        present: false
    },
    heat_pump: {
        present: false
    }
})
const outData = ref<outputData | undefined>()

function fill_unknown_with_default(data: inputData, default_data: inputData) {
    for (const module in default_data) {
        if (data[module] === undefined) {
            data[module] = {};
        }

        for (const key in default_data[module]) {

            if (data[module][key] === undefined) {
                data[module][key] = default_data[module][key];
            }
        }
    }
}

// Funktion, die das Backend aufruft (Dummy Implementation)
const calculateSavings = async () => {
    fill_unknown_with_default(inData.value, defaultData)
    // console.log(fill_unknown_with_default(inData.value))

    isLoading.value = true;
    results.value = null; // Alte Ergebnisse zurücksetzen

    // Validierung (Optional, aber empfohlen)
    //   if (!inputData. || !formData.currentPrice) {
    // 	alert("Bitte geben Sie Jahresverbrauch und aktuellen Preis an.");
    // 	isLoading.value = false;
    // 	return;
    //   }

    try {
        // === HIER WÜRDE DEIN ECHTER BACKEND CALL STEHEN ===
        // const response = await fetch('https://dein-backend.api/v1/calculate', {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(formData)
        // });
        // const data = await response.json();

        // Simulation der Backend-Ladezeit
        await new Promise(resolve => setTimeout(resolve, 1800));
        console.debug(inData.value)
        // Ergebnisse formatieren und im State speichern
        outData.value = {
            oldCost: 15000,
            newCost: 37,
            savings: (15000 - 37),
            avgNewPrice: (37 / 12)
        };

    } catch (error) {
        console.error("Fehler bei der Berechnung", error);
        alert("Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.");
    } finally {
        isLoading.value = false;
    }
};
</script>

<style>
/* Keine Scoped Styles nötig, da alles über Tailwind Klassen gelöst ist. */
/* Falls gewünscht, kann hier die 'Inter' Font eingebunden werden. */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
</style>