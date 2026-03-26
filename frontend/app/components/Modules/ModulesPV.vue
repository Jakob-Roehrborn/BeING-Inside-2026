<template>
    <ModulesBase title="Haben Sie eine PV-Anlage?" v-model="model">
        <div class="flex flex-col gap-4">

            <UtilsInput v-model="model.power" title="installierte Leistung" placeholder="10" , unit="kWp"
                :required="true" />

            <div class="flex flex-row justify-between gap-8">
                <UtilsInput v-model="model.angle" title="Dachneigung" placeholder="30" , unit="°" class="w-2/3" />

                <div class="w-1/3">
                    <label for="consumption" class="text-sm font-medium text-slate-700 mb-1 pl-1.5 w-full">
                        Ausrichtung
                    </label>
                    <div class="relative rounded-md shadow-sm w-full">
                        <select v-model="model.direction" class="w-full px-4 pt-3.5 pb-4 styled-input">
                            <option selected=true value="North">Norden</option>
                            <option value="East">Osten</option>
                            <option value="South">Süden</option>
                            <option value="West">Westen</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { PV } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<PV>({ required: true })

onMounted(() => {
    model.value.direction = "South"
})
</script>