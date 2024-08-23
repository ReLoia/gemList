<script setup lang="ts">
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from '@/store/header.js';
import {onMounted, onUnmounted, ref, shallowRef} from "vue";
import {useRoute} from "vue-router";
import {GameModel} from "@/types/common";

const gamePageHeader = shallowRef(GamePageHeader)
const route = useRoute()
const header = useHeaderStore()

const gameID = route.params.id;
const game = ref<GameModel>(null);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    const response = await fetch(`/api/game/${gameID}`);
    game.value = await response.json();

    header.setExpanded(true)
    header.setContent({
      component: gamePageHeader,
      props: {
        title: game.value.title,
        description: game.value.description,
        // image:
      }
    })
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }

});

onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(null)
})

</script>

<template>

</template>

<style scoped>

</style>