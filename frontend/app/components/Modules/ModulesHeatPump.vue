<template>
    <ModulesBase title="Haben Sie eine Wärmepumpe?" v-model="model">
        <div class="flex justify-between">
            <div>
                <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                    jährlicher Verbrauch
                </label>
                <div class="relative rounded-md shadow-sm">
                    <input type="number" v-model="model.yearly_consumption" placeholder="z.B. 5.000"
                        class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                    <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                        kWh/Jahr
                    </div>
                </div>
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { HeatPump } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<HeatPump>({ required: true })

</script>