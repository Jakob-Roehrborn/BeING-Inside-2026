<template>
    <ModulesBase title="Haben Sie eine PV-Anlage?" v-model="model">
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    installierte Leistung
                </label>
                <div class="relative rounded-md shadow-sm">
                    <input type="number" v-model="model.power" placeholder="z.B. 400"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                    <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        Wp
                    </div>
                </div>
            </div>
        </div>
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    Dachneigung
                </label>
                <div class="relative rounded-md shadow-sm">
                    <input type="number" v-model="model.angle" placeholder="z.B. 30"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                    <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        °
                    </div>
                </div>
            </div>
        </div>
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    Ausrichtung
                </label>
                <div class="relative rounded-md shadow-sm">
                    <select v-model="model.angle" placeholder="z.B. 30"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg">
                        <option selected=true value="North">Norden</option>
                        <option value="East">Osten</option>
                        <option value="South">Süden</option>
                        <option value="West">Westen</option>
                    </select>
                </div>
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { PV } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<PV>({ required: true })

</script>