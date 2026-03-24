<template>
    <div>
        <div class="flex justify-between border-b-2 border-slate-100 pb-2 my-6 bg-slate-100 py-2 px-4 rounded-xl">

            <h2 class="text-lg font-semibold text-slate-900 flex items-center gap-2 ">
                {{props.title}}
            </h2>

            <UtillsYesNoButton v-model="model.present" />
        </div>

        <div v-if="model.present" class="space-y-6">
            <slot />
        </div>
    </div>
</template>

<script lang="ts" setup>
import type { PV, EV, Battery, HeatPump } from '~/types/inputData';
import UtillsYesNoButton from '../Utils/UtillsYesNoButton.vue';

const props = defineProps<{
    title: String
}>()

const model = defineModel<PV | EV | Battery | HeatPump>({ required: true })

</script>