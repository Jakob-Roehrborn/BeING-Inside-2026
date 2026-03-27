<template>
    <div>
        <!-- <UtilsInput v-model="model.zip_code" title="PLZ" input_type="text" :required="true" /> -->

        <div>
            <label class="text-sm font-medium text-slate-700 mb-1 pl-1.5 inline-flex items-center">
                PLZ
                <span class="text-red-500 ml-1 font-bold">*</span>
            </label>

            <div class="relative rounded-md shadow-sm">
                <input v-model="model.postal_code" class="w-full px-4 py-3 text-lg styled-input" />
            </div>

        </div>
             
        <div class="flex flex-col items-center gap-4 bg-slate-50 p-4 rounded-xl my-8">
            <UtilsInput v-model="model.total_consumption" title="Haushaltsstromverbrauch" placeholder="4500"
            unit="kWh/Jahr" :required="true" class="w-full" />
            <UtilPersonSlider class="w-full" v-model="people" />
        </div>
        
        <UtilsInput v-model="model.eprice" title="Bisheriger Stromtarif" placeholder="0.37" unit="€/kWh" />
        
        <div class="my-6"/>

        <div class="flex flex-row justify-between">
            <div class="text-sm font-medium text-slate-700 mb-1 pl-1.5 inline-flex items-center">Achten sie bewusst auf Ihren Stromverbrauch?</div>
            <input v-model="model.smart" type="checkbox" class="mr-2 size-6 accent-sachsenrot">
        </div>
    </div>
</template>

<script lang="ts" setup>
import type { GeneralInfo } from '~/types/inputData';
import UtilPersonSlider from './Utils/UtilPersonSlider.vue';

const CONSUMPTION = [1500, 2500, 3200, 4000, 5000]

const model = defineModel<GeneralInfo>({ required: true })

let ignore_slider = false

watch(() => model.value.total_consumption, () => {
    console.log("WATCH")
    ignore_slider = true
    setTimeout(() => ignore_slider = false, 50)
    let new_people = 0
    for (let i = 0; i < CONSUMPTION.length; i++) {
        if (model.value.total_consumption >= CONSUMPTION[i]!) {
            new_people = i
        }
    }
    people.value = new_people
})

const people = ref(2)

watch(people, () => {
    if (ignore_slider) return
    model.value.total_consumption = CONSUMPTION[people.value]!
})

</script>

<style></style>