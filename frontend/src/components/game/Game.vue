<script setup>
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from "@/store/header.js";
import {onUnmounted} from "vue";

const header = useHeaderStore()

header.setExpanded(true)
header.setContent(GamePageHeader)

onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(null)
})

</script>

<template>

</template>

<style scoped>

</style>