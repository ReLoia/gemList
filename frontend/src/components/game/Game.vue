<script setup lang="ts">
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from '@/store/header.js';
import {onMounted, onUnmounted, ref, shallowRef} from "vue";
import {useRoute} from "vue-router";
import {GameModel} from "@/types/common";
import ExternalLinkItem from "./ui/ExternalLinkItem.vue";
import Card from "../home/ui/carousel/Card.vue";
import SmallGameCard from "../common/SmallGameCard.vue";
import StaffCard from "./ui/StaffCard.vue";

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
    <div class="content">
      <section class="external-links">
        <!--   list of external links related to the game     -->
        <ExternalLinkItem v-for="link in game.externalLinks" :key="link.id" :url="link.url" :img_url="link.img_url"/>

      </section>
      <section class="related">
        <!--   list of related games     -->
        <h2>Related Games</h2>
        <ul>
          <!--          TODO: load related games from backend -->
          <SmallGameCard id="1" img_url="https://via.placeholder.com/150"/>
        </ul>

      </section>
      <section>
        <h2>Staff</h2>
        <ul>
          <StaffCard :staff="{
            id: '1',
            img_url: 'https://via.placeholder.com/150',
            name: 'John Doe',
            role: 'Developer'
          }"/>
          <StaffCard :staff="{
            id: '1',
            img_url: 'https://via.placeholder.com/150',
            name: 'John Doe',
            role: 'Developer'
          }"/>
        </ul>
      </section>

      <divider></divider>

      <!--   stats is a grid that contains "widgets" - div that are N cols of width and that have rounded corners and dark background   -->
      <div class="stats">
        <div class="widget ratings">
          <ul>
            <li>
              <span>1</span>
            </li>
            <li>
              <span>2</span>
            </li>
            <li>
              <span>3</span>
            </li>
            <li>
              <span>4</span>
            </li>
            <li>
              <span>5</span>
            </li>
            <li>
              <span>6</span>
            </li>
            <li>
              <span>7</span>
            </li>
            <li>
              <span>8</span>
            </li>
            <li>
              <span>9</span>
            </li>
            <li>
              <span>10</span>
            </li>
          </ul>
        </div>
      </div>

    </div>
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

  padding-inline: 15px;

  & > .content {
    grid-area: content;

    & > section {
      & > h2 {
        margin-left: 20px;
        margin-top: 20px;
        margin-bottom: 10px;
      }

      & > ul {
        display: flex;
        gap: 10px;
        padding: 0;
        margin: 0;
        list-style: none;
      }

      &.external-links {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
    }

    & > divider {
      display: block;
      height: 1px;
      margin-block: 30px;
      width: 90%;
      margin-inline: auto;

      background: white;
    }

    & > .stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;

      & > .widget {
        border-radius: 6px;
        background: rgba(60, 60, 60, 0.4);
        padding: 6px 20px;

        &.ratings {
          grid-column: span 2;

          & > ul {
            padding: 0;
            margin: 0;
            list-style: none;

            & > li {
              font-size: .85rem;

              & > span {
                display: block;
                width: 26px;
                text-align: center;
                background: red;

                border-radius: 4px;
              }
            }
          }
        }
      }
    }
  }

  & > .metadata {
    grid-area: metadata;

    width: 200px;
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