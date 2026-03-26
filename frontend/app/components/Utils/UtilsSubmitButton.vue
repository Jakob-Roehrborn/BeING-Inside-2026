<template>
    <button
        class="w-full flex justify-center items-center gap-2 py-4 px-6 bg-sachsenrot text-white font-bold rounded-lg shadow-md hover:scale-105 hover:brightness-110 hover:shadow-xl transition-all disabled:opacity-60 disabled:cursor-not-allowed text-lg"
        @click="submit" :disabled="props.isLoading">
        <svg v-if="props.isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
        </svg>
        {{ props.isLoading ? 'Berechnung läuft...' : 'Einsparpotenzial berechnen' }}
    </button>
</template>

<script lang="ts" setup>

const props = defineProps<{
    isLoading: boolean
}>()

const emits = defineEmits(["submit"])

function submit() {
    emits("submit")
}

</script>

<style>

</style>