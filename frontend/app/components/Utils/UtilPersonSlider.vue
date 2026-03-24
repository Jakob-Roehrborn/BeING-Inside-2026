<template>
    <div class="bg-slate-50 p-6 rounded-xl border border-slate-100">
        <label for="shiftable" class="text-base font-semibold text-slate-800 mb-3 flex justify-between items-center">
            Haushaltsgröße
        </label>
        <div class="flex flex-row justify-between px-2">
            <UtilPersonIcon :active="active" v-for="active in activePersons" class="size-8" />
        </div>
        <input type="range" v-model="people" min="0" max="4"
            class="w-full bg-slate-200 rounded-lg cursor-pointer accent-sachsenrot h-2 px-4" />
        <p class="mt-3 text-sm text-slate-400 leading-relaxed">
            Wir benutzen diese Angabe, um Ihren jährlichen Stromverbrauch zu schätzen
        </p>
        <p class="mt-3 text-[0.25em] text-slate-200 leading-relaxed">
            Und um zu wissen, mit wie vielen Kugeln wir unsere Pistole laden müssen, wenn sie nicht zahlen :)
        </p>
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