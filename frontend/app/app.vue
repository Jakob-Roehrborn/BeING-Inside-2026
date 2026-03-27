<template>
    <div class="min-h-screen bg-slate-50 text-slate-900 antialiased py-10 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">

            <header class="text-center mb-12">
                <Header />
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">

                <InputForm v-model="inData" :is-loading="isLoading" @submit="calculateSavings" />

                <!-- <Output :is-loading="isLoading" , :results="outData" /> -->
                <ResultDashboard :is-loading="isLoading" :results="outData"/>

            </div>

        </div>
    </div>
</template>

<script lang="ts" setup>
import ResultDashboard from './components/ResultDashboard.vue';
import type inputData from './types/inputData';
import { defaultData } from './types/inputData';
import type outputData from './types/outputData';
import { io } from 'socket.io-client'

// // State für UI
const isLoading = ref(false);
const results = ref();

const inData = ref<inputData>({
    general_info: {
        smart: false
    },
    memory: {
        exist: false
    },
    ecar: {
        exist: false,
        wallbox: false
    },
    solar_system: {
        exist: false
    },
    heat_pump: {
        exist: false
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

    isLoading.value = true;
    results.value = null; // Alte Ergebnisse zurücksetzen

    // Validierung (Optional, aber empfohlen)
    //   if (!inputData. || !formData.currentPrice) {
    // 	alert("Bitte geben Sie Jahresverbrauch und aktuellen Preis an.");
    // 	isLoading.value = false;
    // 	return;
    //   }

    try {
        const response = await fetch('http://localhost:5000/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(inData.value)
        });
        const data = await response.json();

        // // Simulation der Backend-Ladezeit
        // await new Promise(resolve => setTimeout(resolve, 1800));
        // console.debug(inData.value)
        // // Ergebnisse formatieren und im State speichern
        // outData.value = {
        //     oldCost: 15000,
        //     newCost: 37,
        //     savings: (15000 - 37),
        //     avgNewPrice: (37 / 12)
        // };

        outData.value = data

    } catch (error) {
        console.error("Fehler bei der Berechnung", error);
        alert("Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.");
    } finally {
        isLoading.value = false;
    }

};

// Reactive state variables
const isConnected = ref(false)
let socket = null

onMounted(() => {
    socket = io('http://localhost:5000')

    socket.on('connect', () => {
        isConnected.value = true
        console.log('Successfully connected to Flask server')
    })

    socket.on('disconnect', () => {
        isConnected.value = false
        console.log('Disconnected from Flask server')
    })

    socket.on('module_change', (payload) => {
        console.log('Received from server:', payload)
        let module: number = payload["module"]
        let state: boolean = Boolean(payload["state"])
        console.log('mod', module, "state", state)
        // #Module = [PV, EV, WP, Batterie]
        switch (module) {
            case 0: {
                inData.value.solar_system.exist = state
                break
            }
            case 1: {
                inData.value.ecar.exist = state
                break
            }
            case 2: {
                inData.value.heat_pump.exist = state
                break
            }
            case 3: {
                inData.value.memory.exist = state
                break
            }
        }
    })
})

// Clean up the connection when the component is destroyed
onBeforeUnmount(() => {
    if (socket) {
        socket.disconnect()
    }
})

// Function to trigger a custom event back to Flask
const sendMessageToFlask = () => {
    if (socket && isConnected.value) {
        socket.emit('client_message', { msg: 'Hello from the Nuxt frontend!' })
    }
}
</script>

<style>
/* Keine Scoped Styles nötig, da alles über Tailwind Klassen gelöst ist. */
/* Falls gewünscht, kann hier die 'Inter' Font eingebunden werden. */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
</style>