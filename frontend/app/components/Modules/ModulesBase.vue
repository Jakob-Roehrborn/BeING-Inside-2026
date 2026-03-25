<template>
    <div>
        <div class="flex justify-between shadow pb-2 mb-4 mt-8 bg-slate-100 py-2 px-4 rounded-xl">

            <h2 class="text-lg font-semibold text-slate-900 flex items-center gap-2">
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