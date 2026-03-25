<template>
    <ModulesBase title="Haben Sie eine Wärmepumpe?" v-model="model">
        <UtilsInput v-model="model.yearly_consumption" title="jährlicher Verbrauch" placeholder="5.000" unit="kWh/Jahr"/>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { HeatPump } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<HeatPump>({ required: true })

</script>