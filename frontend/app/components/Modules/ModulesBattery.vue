<template>
    <ModulesBase title="Haben Sie einen Batteriespeicher?" v-model="model">
        <UtilsInput v-model="model.capacity" title="Speicherkapazität" placeholder="10" unit="kWh"/>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { Battery } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<Battery>({ required: true })

</script>