<template>
    <ModulesBase title="Haben Sie einen Batteriespeicher?" v-model="model">
        <div>
            <UtilsInput v-model="model.capacity_kWh" title="Speicherkapazität" placeholder="10" unit="kWh" :required="true"/>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { Memory } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<Memory>({ required: true })

</script>