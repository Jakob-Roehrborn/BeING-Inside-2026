<template>
    <ModulesBase title="Haben Sie ein Elektroauto?" v-model="model">
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                   jährliche Fahrstrecke
                </label>
                <div class="relative rounded-md shadow-sm">
                    <input type="number" v-model="model.milage" placeholder="z.B. 15.500"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                    <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        Km
                    </div>
                </div>
            </div>
        </div>
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    typischer Ladezeitpunkt
                </label>
                <div class="relative rounded-md shadow-sm">
                    <input type="number" v-model="model.charging_time" placeholder="00:00"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                </div>
            </div>
        </div>
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    Leistung der Ladeeinrichtung
                </label>
                <div class="relative rounded-md shadow-sm">
                    <input type="number" v-model="model.charging_power" placeholder="z.B. 11"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                    <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        kW
                    </div>
                </div>
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { EV } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<EV>({ required: true })

</script>