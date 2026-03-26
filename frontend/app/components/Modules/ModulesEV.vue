<template>
    <ModulesBase title="Haben Sie ein Elektroauto?" v-model="model">
        <div class="flex flex-col gap-4">
            <UtilsInput v-model="model.ziel_jahreskilometer" title="jährliche Fahrstrecke" placeholder="15.500" unit="km"
                :required="true" />
            <div class="flex flex-row justify-between">
                <div class="font-semibold">Benutzen Sie eine Wallbox zum Laden ihres Elektroautos?</div>
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