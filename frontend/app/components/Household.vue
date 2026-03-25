<template>
    <div>
        <UtilsInput v-model="model.zip_code" title="PLZ" />

        <div class="my-6"/>

        <div class="flex flex-col items-center gap-4 bg-slate-50 p-4 rounded-xl">
            <UtilsInput v-model="model.consumption" title="Geschätzter Jahresstromverbrauch" placeholder="4500" unit="kWh/Jahr"
            class="w-full"/> 
            <UtilPersonSlider class="w-full" v-model="people"/>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type { Household } from '~/types/inputData';
import UtilPersonSlider from './Utils/UtilPersonSlider.vue';

const CONSUMPTION = [1500, 2500, 3200, 4000, 5000]

const model = defineModel<Household>({ required: true })

let ignore_slider = false

watch(() => model.value.consumption, () => {
    console.log("WATCH")
    ignore_slider = true
    setTimeout(()=>ignore_slider = false, 50)
    for (let i = 0; i < CONSUMPTION.length; i++) {
        if (CONSUMPTION[i]! >= model.value.consumption) {
            people.value = i
            return;
        }
    }
    people.value = CONSUMPTION.length
})

const people = ref(2)

watch(people, () => {
    if (ignore_slider) return
    model.value.consumption = CONSUMPTION[people.value]!
})

</script>

<style></style>