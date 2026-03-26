<template>
    <div class="p-4 rounded-xl border border-slate-300 shadow-sm">
        <label class="text-base font-semibold text-slate-800 mb-3 flex justify-between items-center">
            Haushaltsgröße
        </label>
        <div class="flex flex-row justify-between px-2">
            <UtilPersonIcon :active="active" v-for="active in activePersons" class="size-6" />
        </div>
        <input type="range" v-model.number="people" min="0" max="4"
            class="w-full rounded-lg cursor-pointer accent-sachsenrot h-2 px-4 animated-slider" />
    </div>
</template>

<script lang="ts" setup>
import UtilPersonIcon from './UtilPersonIcon.vue'


const people = defineModel<number>()

const activePersons = computed(() => { 
    let list = [false, false, false, false, false]

    for (let i = 0; i <= people.value!; i++) {
        list[i] = true
    }

    return list
})

</script>

<style>
</style>