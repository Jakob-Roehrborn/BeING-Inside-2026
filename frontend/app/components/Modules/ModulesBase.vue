<template>
    <div>
        <div class="flex justify-between shadow pb-2 mb-4 mt-8 bg-slate-100 py-2 px-4 rounded-xl">

            <h2 class="text-lg font-semibold text-slate-900 flex items-center gap-2">
                {{props.title}}
            </h2>

            <UtillsYesNoButton v-model="model.present" />
        </div>

        <slot v-if="model.present"/>
    </div>
</template>

<script lang="ts" setup>
import type { SolarSystem, ECar, Memory, HeatPump } from '~/types/inputData';
import UtillsYesNoButton from '../Utils/UtillsYesNoButton.vue';

const props = defineProps<{
    title: String
}>()

const model = defineModel<SolarSystem | ECar | Memory | HeatPump>({ required: true })

</script>