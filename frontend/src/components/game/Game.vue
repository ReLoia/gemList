<script setup>
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from "@/store/header.js";
import {onUnmounted, shallowRef} from "vue";

const gamePageHeader = shallowRef(GamePageHeader)

const header = useHeaderStore()
header.setExpanded(true)
header.setContent({
  component: gamePageHeader,
  props: {
    title: 'Game Title',
    description: 'Game Description',
    image: 'https://via.placeholder.com/200'
  }
})

onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(null)
})

</script>

<template>

</template>

<style scoped>

</style>