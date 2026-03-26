<template>
    <ModulesBase title="Haben Sie ein Elektroauto?" v-model="model">
        <div class="flex flex-col gap-4">
            <UtilsInput v-model="model.ziel_jahreskilometer" title="jährliche Fahrstrecke" placeholder="15.500"
                unit="km" :required="true" />
            <UtilsInput v-model="model.verbrauch_kwh_pro_100km" title="Verbrauch" placeholder="14" unit="kWh/100km" />
            <UtilsInput v-model="model.akku_grosse" title="Größe der Batterie" placeholder="64" unit="kWh" />
            <UtilsTimeInput v-model="model.start_ladezeit" label="Zu welcher Zeit fangen Sie normalerweise an, Ihr Auto zu laden?"/>
            <div class="flex flex-row justify-between">
                <div class="text-sm font-medium text-slate-700 mb-1 pl-1.5 inline-flex items-center">Benutzen Sie eine Wallbox zum Laden ihres Elektroautos?</div>
                <input v-model="model.wallbox" type="checkbox" class="mr-2 size-6 accent-sachsenrot">
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { ECar } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<ECar>({ required: true })

</script>