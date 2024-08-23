<script setup lang="ts">
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from '@/store/header.js';
import {onMounted, onUnmounted, ref, shallowRef} from "vue";
import {useRoute} from "vue-router";
import {GameModel} from "@/types/common";
import ExternalLinkItem from "./ui/ExternalLinkItem.vue";

const gamePageHeader = shallowRef(GamePageHeader)
const route = useRoute()
const header = useHeaderStore()

const gameID = route.params.id;
// TODO: reset to null
const game = ref<GameModel>({
  id: '',
  title: 'a',
  description: 'b',
  externalLinks: [
    {
      url: 'http://localhost:8080',
      img_url: 'https://via.placeholder.com/150'
    },
    {
      url: 'http://localhost:8080',
      img_url: 'https://via.placeholder.com/150'
    }
  ]
});
const error = ref<string | null>(null);


onMounted(async () => {
  header.setExpanded(true);
  header.setLoading(true);

  try {
    const response = await fetch(`/api/game/${gameID}`);
    game.value = await response.json();
  } catch (e) {
    error.value = e.message;
  } finally {
    header.setLoading(false);
  }

  header.setContent({
    component: gamePageHeader,
    props: {
      title: game?.value?.title,
      description: game?.value?.description,
      // image:
    }
  })
});


onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(() => null)
})

// TODO: remove metadata template:
const metadata = [{
  name: 'Rating',
  value: '4.5'
}, {
  name: 'Likes',
  value: '100'
}, {
  name: 'Downloads',
  value: '1000'
}]

</script>

<template>
  <div class="page" v-if="game">
    <section class="content">
      <div class="external-links">
        <!--   list of external links related to the game     -->
        <ExternalLinkItem v-for="link in game.externalLinks" :key="link.id" :url="link.url" :img_url="link.img_url"/>

      </div>

    </section>
    <div class="metadata">
      <!--   TODO: add more metadata about the game   -->
      <div class="meta" v-for="item in metadata" :key="item.name">
        <span class="name">{{ item.name }}</span>
        <span class="value">{{ item.value }}</span>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  display: grid;
  grid-template-columns: 3fr auto;
  grid-template-areas: "content metadata";
  gap: 5px;

  width: 100%;
  height: 100%;
  max-width: 1400px;
  margin: auto;

  //background: red;


  & > .content {
    grid-area: content;

    & > .external-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
  }

  & > .metadata {
    grid-area: metadata;

    width: 220px;
    padding: 8px 12px;
    min-height: 400px;
    height: fit-content;
    background: rgba(60, 60, 60, 0.4);

    border-radius: 6px;
    font-size: .9em;

    & > .meta {
      margin-bottom: 10px;

      & > span {
        display: block;

        &.name {
          font-weight: bold;
          color: #fff;
          font-size: 1em;
          margin-left: -2px;
        }
      }
    }
  }
}
</style>