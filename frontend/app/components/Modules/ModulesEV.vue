<template>
    <ModulesBase title="Haben Sie ein Elektroauto?" v-model="model">
        <div class="flex flex-col gap-4">
            <UtilsInput v-model="model.milage" title="jährliche Fahrstrecke" placeholder="15.500" unit="km"
                :required="true" />
            <div class="flex flex-row justify-between">
                <div class="font-semibold">Benutzen Sie eine Wallbox zum Laden ihres Elektroautos?</div>
                <input v-model="model.has_wall_box" type="checkbox" class="mr-2 size-6 accent-sachsenrot">
            </div>
        </div>
    </ModulesBase>
</template>

<script lang="ts" setup>
import type { EV } from '~/types/inputData';
import ModulesBase from './ModulesBase.vue';


const model = defineModel<EV>({ required: true })

</script>