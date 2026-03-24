<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 antialiased py-10 px-4 sm:px-6 lg:px-8">
	<div class="max-w-7xl mx-auto">
	  
	  <header class="text-center mb-12">
		<Header />
	  </header>

	  <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">
		
		<InputForm v-model="inputData!" :is-loading="isLoading" @submit="calculateSavings"/>
		
		<Output :is-loading="isLoading", :results="outputData!" />
		
	  </div>

	</div>
  </div>
</template>

<script lang="ts" setup>
import type inputData from './types/inputData';
import type outputData from './types/outputData';


// State für UI
const isLoading = ref(false);
const results = ref(null);

const inputData = ref<inputData>()
const outputData = ref<outputData>()

// Funktion, die das Backend aufruft (Dummy Implementation)
const calculateSavings = async () => {
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

	// Ergebnisse formatieren und im State speichern
	outputData.value = {
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