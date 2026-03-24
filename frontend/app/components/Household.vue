<template>
    <div>
        <h2 class="text-2xl font-semibold text-slate-900 flex items-center gap-2 border-b-2 border-slate-100 pb-3 mb-6">
            Ihre aktuellen Stromdaten
        </h2>

        <div class="space-y-6">
            <div class="flex justify-between">
                <div class="form-group">
                    <label for="consumption" class="block text-sm font-medium text-slate-700 mb-1">
                        Geschätzter Jahresstromverbrauch
                    </label>
                    <div class="relative rounded-md shadow-sm">
                        <input type="number" id="consumption" v-model="model.consumption"
                            placeholder="z.B. 4500"
                            class="block w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition duration-150 text-lg" />
                        <div
                            class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-slate-500">
                            kWh/Jahr
                        </div>
                    </div>
                </div>
                <div></div>
            </div>

            <UtilPersonSlider v-model="people"/>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type { Household } from '~/types/inputData';
import UtilPersonSlider from './Utils/UtilPersonSlider.vue';

const model = defineModel<Household>({required: true})

const people = ref(2)

watch(people, () => {
    const CONSUMPTION = [1500, 2500, 3200, 4000, 5000] 
    model.value.consumption = CONSUMPTION[people.value]!
})

</script>

<style></style>