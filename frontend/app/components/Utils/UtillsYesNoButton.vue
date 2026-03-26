<template>
    <div class="flex items-center gap-4">
        <label class="flex items-center gap-2 cursor-pointer">
            <span>Ja</span>
            <input type="checkbox" :value="false" v-model="yesSelected"
                class="size-4 cursor-pointer accent-sachsenrot align-middle">
        </label>

        <label class="flex items-center gap-2 cursor-pointer">
            <span>Nein</span>
            <input type="checkbox" :value="true" v-model="noSelected"
                class="size-4 cursor-pointer accent-sachsenrot align-middle">
        </label>
    </div>
</template>

<script lang="ts" setup>

const yesSelected = ref(false)
const noSelected = ref(true)

const model = defineModel<boolean>({required: true})

watch(model, (state) => {
    if (state) {
        yesSelected.value = true
        noSelected.value = false
    }
    else {
        yesSelected.value = false
        noSelected.value = true
    }
})

watch(yesSelected, (yes) => {
    if (yes) {
        noSelected.value = false
        model.value = true
    }
    else {
        noSelected.value = true
        model.value = false
    }
})
watch(noSelected, (no) => {
    if (no) {
        yesSelected.value = false 
        model.value = false
    }
    else {
        yesSelected.value = true
        model.value = true
    }
})

</script>