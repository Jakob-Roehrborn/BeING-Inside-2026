<template>
  <div class="calculator-container">
    <header class="header">
      <h1>Dynamischer Stromtarif-Rechner</h1>
      <p>Finden Sie heraus, wie viel Sie mit einem dynamischen Tarif sparen können, indem Sie Ihren Verbrauch in günstige Zeiten verlegen.</p>
    </header>

    <div class="main-content">
      <section class="input-section card">
        <h2>1. Ihre Daten</h2>
        
        <div class="form-group">
          <label for="consumption">Jahresverbrauch (kWh)</label>
          <input type="number" id="consumption" v-model="formData.consumption" placeholder="z.B. 4500" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="currentPrice">Aktueller Preis (Ct/kWh)</label>
            <input type="number" id="currentPrice" v-model="formData.currentPrice" step="0.1" placeholder="z.B. 32.5" />
          </div>
          <div class="form-group">
            <label for="baseFee">Grundgebühr (€/Monat)</label>
            <input type="number" id="baseFee" v-model="formData.baseFee" placeholder="z.B. 12" />
          </div>
        </div>

        <hr />

        <h2>2. Ihre Flexibilität</h2>
        <div class="toggles">
          <label class="toggle-label">
            <input type="checkbox" v-model="formData.hasEV" /> E-Auto vorhanden
          </label>
          <label class="toggle-label">
            <input type="checkbox" v-model="formData.hasHeatPump" /> Wärmepumpe vorhanden
          </label>
          <label class="toggle-label">
            <input type="checkbox" v-model="formData.hasBattery" /> Batteriespeicher
          </label>
        </div>

        <div class="form-group slider-group">
          <label for="shiftable">Verschiebbarer Verbrauch: <strong>{{ formData.shiftablePercentage }}%</strong></label>
          <input type="range" id="shiftable" v-model="formData.shiftablePercentage" min="0" max="100" />
          <small>Wie viel Strom können Sie gezielt dann nutzen, wenn er günstig ist?</small>
        </div>

        <button 
          class="btn-calculate" 
          @click="calculateSavings" 
          :disabled="isLoading"
        >
          {{ isLoading ? 'Berechne Daten...' : 'Einsparpotenzial berechnen' }}
        </button>
      </section>

      <section class="result-section card" :class="{ 'is-blurred': !results && !isLoading }">
        <h2>Ihr Ergebnis</h2>
        
        <div v-if="isLoading" class="loading-spinner">
          Lade Daten vom Backend...
        </div>

        <div v-else-if="results" class="results-content">
          <div class="highlight-box">
            <h3>Mögliche Ersparnis pro Jahr</h3>
            <span class="savings-amount">{{ results.savingsEuro }} €</span>
          </div>

          <div class="comparison-table">
            <div class="row">
              <span>Bisherige Kosten (geschätzt):</span>
              <strong>{{ results.oldCost }} €</strong>
            </div>
            <div class="row">
              <span>Kosten Dynamischer Tarif:</span>
              <strong class="text-green">{{ results.newCost }} €</strong>
            </div>
            <div class="row">
              <span>Durchschnittlicher Preis neu:</span>
              <strong>{{ results.avgNewPrice }} Ct/kWh</strong>
            </div>
          </div>
          
          <div class="chart-placeholder">
            [ Hier könnte ein Balkendiagramm (Alt vs. Neu) eingebunden werden ]
          </div>
          
          <p class="disclaimer">
            *Dies ist eine Schätzung basierend auf historischen Day-Ahead-Börsenpreisen und Ihrem angegebenen Flexibilitätsprofil.
          </p>
        </div>

        <div v-else class="empty-state">
          Bitte geben Sie links Ihre Daten ein und klicken Sie auf Berechnen.
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// State für Eingabedaten
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

// Funktion, die das Backend aufruft
const calculateSavings = async () => {
  isLoading.value = true;
  results.value = null;

  try {
    // HIER WÜRDE DEIN BACKEND CALL STEHEN
    // const response = await fetch('/api/calculate-dynamic-tariff', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(formData)
    // });
    // const data = await response.json();

    // Simulation der Backend-Ladezeit und Dummy-Antwort
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Dummy Daten (als Antwort vom Backend)
    const oldCostAnnual = (formData.consumption * (formData.currentPrice / 100)) + (formData.baseFee * 12);
    // Erfundene Logik für Dummy-Ergebnis: Besserer Preis durch Flexibilität
    const reduction = 1 - (formData.shiftablePercentage * 0.005); 
    const newCostAnnual = oldCostAnnual * reduction - 120; // -120€ Bonus z.B.

    results.value = {
      oldCost: oldCostAnnual.toFixed(2),
      newCost: newCostAnnual.toFixed(2),
      savingsEuro: (oldCostAnnual - newCostAnnual).toFixed(2),
      avgNewPrice: (formData.currentPrice * reduction).toFixed(1)
    };

  } catch (error) {
    console.error("Fehler bei der Berechnung", error);
    alert("Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Basis Styling für eine saubere, moderne UI */
.calculator-container {
  max-width: 1000px;
  margin: 0 auto;
  font-family: 'Inter', system-ui, sans-serif;
  color: #333;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.1);
}

h2 {
  margin-top: 0;
  font-size: 1.25rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

label {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

input[type="number"] {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.toggles {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.toggle-label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 10px;
}

.slider-group small {
  color: #666;
  margin-top: 5px;
}

.btn-calculate {
  width: 100%;
  padding: 14px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-calculate:hover:not(:disabled) {
  background-color: #004494;
}

.btn-calculate:disabled {
  background-color: #999;
  cursor: not-allowed;
}

.is-blurred {
  opacity: 0.6;
}

.highlight-box {
  background-color: #e8f5e9;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  margin-bottom: 25px;
}

.highlight-box h3 {
  margin: 0 0 10px 0;
  color: #2e7d32;
  font-size: 1rem;
}

.savings-amount {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1b5e20;
}

.comparison-table .row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.text-green {
  color: #2e7d32;
}

.chart-placeholder {
  height: 150px;
  background: #f9f9f9;
  border: 2px dashed #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 25px 0;
  color: #888;
  border-radius: 8px;
  text-align: center;
  padding: 20px;
}

.disclaimer {
  font-size: 0.8rem;
  color: #777;
  line-height: 1.4;
}

.empty-state, .loading-spinner {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}
</style>