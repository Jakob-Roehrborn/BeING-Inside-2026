<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 antialiased py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      
      <header class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-slate-950 tracking-tight sm:text-5xl">
          Dynamischer <span class="text-blue-600">Stromtarif-Rechner</span>
        </h1>
        <p class="mt-4 text-xl text-slate-600 max-w-3xl mx-auto">
          Ermitteln Sie Ihr jährliches Einsparpotenzial, indem Sie Ihren Stromverbrauch durch einen dynamischen Tarif intelligent in günstige Stunden verlegen.
        </p>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">
        
        <section class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100">
          <div class="space-y-10">
            
            <div>
              <h2 class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3 mb-6">
                <span class="text-blue-500 font-mono text-xl">1</span>
                Ihre aktuellen Stromdaten
              </h2>
              
              <div class="space-y-6">
                <div class="form-group">
                  <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    Geschätzter Jahresstromverbrauch
                  </label>
                  <div class="relative rounded-md shadow-sm">
                    <input 
                      type="number" id="consumption" v-model="formData.consumption" placeholder="z.B. 4500"
                      class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg"
                    />
                    <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                      kWh/Jahr
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div class="form-group">
                    <label for="currentPrice" class="block text-sm font-medium text-slate-700 mb-1">
                      Aktueller Arbeitspreis
                    </label>
                    <div class="relative rounded-md shadow-sm">
                      <input 
                        type="number" id="currentPrice" v-model="formData.currentPrice" step="0.1" placeholder="z.B. 32.5"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition text-lg"
                      />
                      <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        Ct/kWh
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="baseFee" class="block text-sm font-medium text-slate-700 mb-1">
                      Monatliche Grundgebühr
                    </label>
                    <div class="relative rounded-md shadow-sm">
                      <input 
                        type="number" id="baseFee" v-model="formData.baseFee" placeholder="z.B. 12"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition text-lg"
                      />
                      <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        €/Monat
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <hr class="border-slate-100" />

            <div>
              <h2 class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3 mb-6">
                <span class="text-blue-500 font-mono text-xl">2</span>
                Ihre Flexibilitätspotenziale
              </h2>
              
              <div class="space-y-3 mb-8">
                <label class="flex items-center gap-4 p-4 border rounded-xl border-slate-200 hover:bg-slate-50 cursor-pointer transition">
                  <input type="checkbox" v-model="formData.hasEV" class="h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                  <span class="text-base text-slate-800">Ich besitze ein <strong>Elektroauto</strong></span>
                </label>
                <label class="flex items-center gap-4 p-4 border rounded-xl border-slate-200 hover:bg-slate-50 cursor-pointer transition">
                  <input type="checkbox" v-model="formData.hasHeatPump" class="h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                  <span class="text-base text-slate-800">Ich nutze eine <strong>Wärmepumpe</strong></span>
                </label>
                <label class="flex items-center gap-4 p-4 border rounded-xl border-slate-200 hover:bg-slate-50 cursor-pointer transition">
                  <input type="checkbox" v-model="formData.hasBattery" class="h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                  <span class="text-base text-slate-800">Ich habe einen <strong>Batteriespeicher</strong></span>
                </label>
              </div>

              <div class="form-group bg-slate-50 p-6 rounded-xl border border-slate-100">
                <label for="shiftable" class="block text-base font-semibold text-slate-800 mb-3 flex justify-between items-center">
                  Verschiebbarer Jahresverbrauch
                  <span class="text-3xl font-bold text-blue-600">{{ formData.shiftablePercentage }}%</span>
                </label>
                <input 
                  type="range" id="shiftable" v-model="formData.shiftablePercentage" min="0" max="100" 
                  class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <p class="mt-3 text-sm text-slate-600 leading-relaxed">
                  Schätzen Sie, wie viel Prozent Ihres Gesamtverbrauchs Sie gezielt in günstige Zeiten (z.B. Nachts, Mittags bei Sonne) verlegen können (Laden, Heizen, Waschen).
                </p>
              </div>
            </div>

            <button 
              class="w-full flex justify-center items-center gap-2 py-4 px-6 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-60 disabled:cursor-not-allowed text-lg"
              @click="calculateSavings" 
              :disabled="isLoading"
            >
              <svg v-if="isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isLoading ? 'Berechnung läuft...' : 'Einsparpotenzial berechnen' }}
            </button>
          </div>
        </section>

        <section 
          class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100 transition-all duration-300"
          :class="{ 'opacity-60 pointer-events-none': !results && !isLoading }"
        >
          <h2 class="text-2xl font-semibold text-slate-900 border-b-2 border-slate-100 pb-3 mb-8">
            Ihr geschätztes Ergebnis
          </h2>
          
          <div v-if="isLoading" class="text-center py-16 text-slate-600 space-y-4">
            <svg class="animate-spin h-10 w-10 text-blue-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-lg">Frage Backend-Daten ab...</p>
          </div>

          <div v-else-if="results" class="space-y-10">
            <div class="bg-green-50 border border-green-200 rounded-xl p-6 text-center shadow-inner">
              <h3 class="text-sm font-medium text-green-800 uppercase tracking-wider mb-2">Mögliche Ersparnis pro Jahr*</h3>
              <div class="text-5xl font-extrabold text-green-900 leading-none">
                {{ results.savingsEuro }} <span class="text-4xl font-bold">€</span>
              </div>
            </div>

            <div class="space-y-4">
              <h4 class="text-lg font-semibold text-slate-800">Kostenvergleich im Detail</h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center py-3 px-4 bg-slate-50 rounded-lg border border-slate-100">
                  <span class="text-slate-600">Bisherige Kosten (geschätzt):</span>
                  <span class="font-semibold text-slate-900">{{ results.oldCost }} €</span>
                </div>
                <div class="flex justify-between items-center py-3 px-4 bg-blue-50 rounded-lg border border-blue-100">
                  <span class="text-blue-900 font-medium">Kosten Dynamischer Tarif:</span>
                  <span class="font-bold text-green-700 text-lg">{{ results.newCost }} €</span>
                </div>
                <div class="flex justify-between items-center py-3 px-4 bg-slate-50 rounded-lg border border-slate-100 text-sm">
                  <span class="text-slate-600">Effektiver Arbeitspreis neu:</span>
                  <span class="font-medium text-slate-800">{{ results.avgNewPrice }} Ct/kWh</span>
                </div>
              </div>
            </div>
            
            <div class="h-40 bg-slate-50 border-2 border-dashed border-slate-200 flex items-center justify-center my-8 text-slate-400 rounded-xl px-4 text-center text-sm">
              [ Hier könnte ein Balkendiagramm (Alt vs. Neu) eingebunden werden ]
            </div>
            
            <div class="bg-amber-50 border-l-4 border-amber-300 p-4 rounded-r-lg text-amber-900 text-xs leading-relaxed mt-10">
              <p class="font-semibold mb-1">Hinweis zur Berechnung:</p>
              *Dies ist eine unverbindliche Schätzung basierend auf Ihrem angegebenen Jahresverbrauch und Ihrem Flexibilitätsprofil. Die Berechnung nutzt historische Day-Ahead-Börsenstrompreise (Spotmarkt) des vergangenen Jahres inkl. anfallender Steuern, Abgaben und Netzentgelte. Die tatsächliche Ersparnis hängt stark von Ihrem realen Verbrauchsverhalten ab.
            </div>
          </div>

          <div v-else class="text-center py-20 px-6 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 text-slate-500 space-y-4">
            <svg class="w-16 h-16 mx-auto text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 002-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            <p class="text-lg">Bitte füllen Sie die Daten auf der linken Seite aus und klicken Sie auf <strong>"Berechnen"</strong>, um Ihr Ergebnis zu sehen.</p>
          </div>
        </section>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// State für Eingabedaten (Defaults)
const formData = reactive({
  consumption: 4500,
  currentPrice: 32.5,
  baseFee: 15,
  hasEV: false,
  hasHeatPump: false,
  hasBattery: false,
  shiftablePercentage: 20
});

// State für UI
const isLoading = ref(false);
const results = ref(null);

// Funktion, die das Backend aufruft (Dummy Implementation)
const calculateSavings = async () => {
  isLoading.value = true;
  results.value = null; // Alte Ergebnisse zurücksetzen

  // Validierung (Optional, aber empfohlen)
  if (!formData.consumption || !formData.currentPrice) {
    alert("Bitte geben Sie Jahresverbrauch und aktuellen Preis an.");
    isLoading.value = false;
    return;
  }

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

    // Dummy Daten Logic (Ersetze dies durch Backend-Antwort)
    const oldCostAnnual = (formData.consumption * (formData.currentPrice / 100)) + (formData.baseFee * 12);
    
    // Einfache Dummy-Formel: Je mehr Flexibilität, desto besser der neue Preis
    // (Basis-Ersparnis 10% + Flexibilitätseinfluss)
    const factorFlex = formData.shiftablePercentage * 0.002; // max 0.2 (20%)
    const factorHardware = (formData.hasEV ? 0.05 : 0) + (formData.hasHeatPump ? 0.08 : 0);
    const reduction = 0.10 + factorFlex + factorHardware; // Z.B. ca. 10% - 43% Ersparnis

    const newAvgPrice = formData.currentPrice * (1 - reduction);
    const newCostAnnual = (formData.consumption * (newAvgPrice / 100)) + (10 * 12); // Angenommene neue Grundgebühr 10€

    // Ergebnisse formatieren und im State speichern
    results.value = {
      oldCost: oldCostAnnual.toFixed(2),
      newCost: newCostAnnual.toFixed(2),
      savingsEuro: (oldCostAnnual - newCostAnnual).toFixed(2),
      avgNewPrice: newAvgPrice.toFixed(1)
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