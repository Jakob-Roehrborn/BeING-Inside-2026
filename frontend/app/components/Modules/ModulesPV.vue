<template>
    <ModulesBase title="Haben Sie eine PV-Anlage?" v-model="model">
        <div class="flex flex-col gap-4">

            <UtilsInput v-model="model.capacity_kwp" title="installierte Leistung" placeholder="6" , unit="kWp"
                :required="true" />

            <div class="flex flex-row justify-between gap-8">
                <UtilsInput v-model="model.tilt" title="Neigung der Solaranlage" placeholder="30" , unit="°" class="w-2/3" />

                <div class="w-1/3">
                    <label class="text-sm font-medium text-slate-700 mb-1 pl-1.5 w-full">
                        Ausrichtung
                    </label>
                    <div class="relative rounded-md shadow-sm w-full">
                        <select v-model="model.azimuth" class="w-full px-4 pt-3.5 pb-4 styled-input">
                            <option selected=true value="0">Norden</option>
                            <option value="90">Osten</option>
                            <option value="180">Süden</option>
                            <option value="270">Westen</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { SolarSystem } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<SolarSystem>({ required: true })

onMounted(() => {
    model.value.azimuth = 90
})
</script>