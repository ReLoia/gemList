<script setup lang="ts">
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from "../../store/header";
import {onMounted, onUnmounted, ref, shallowRef} from "vue";
import {useRoute} from "vue-router";
import {GameModel} from "../../types/common";
import ExternalLinkItem from "./ui/ExternalLinkItem.vue";
import SmallGameCard from "../common/SmallGameCard.vue";
import StaffCard from "./ui/StaffCard.vue";
import AchievementItem from "./ui/AchievementItem.vue";
import {BackendApiService} from "../../data/remote/BackendApiService";

const gamePageHeader = shallowRef(GamePageHeader)
const route = useRoute()
const header = useHeaderStore()

const gameID: string = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id;

// TODO: remove placeholder data
const game = ref<GameModel>({
      image: "https://steamcdn-a.akamaihd.net/steam/apps/292030/header.jpg?t=1631046447",
      id: '66cdb5a1055b02fda758c0f6',
      title: 'The Witcher 3: Wild Hunt',
      description: 'The Witcher 3: Wild Hunt is a 2015 action role-playing game developed and published by CD Projekt. Based on The Witcher series of fantasy novels by Andrzej Sapkowski, it is the sequel to the 2011 game The Witcher 2: Assassins of Kings. Played in an open world with a third-person perspective, players control protagonist Geralt of Rivia, a monster hunter known as a witcher, who is looking for his missing adopted daughter on the run from the Wild Hunt: an otherworldly force determined to capture and use her powers.',
      externalLinks: [{
        url: 'http://localhost:8080',
        img_url: 'https://via.placeholder.com/150'
      }, {url: 'http://localhost:8080', img_url: 'https://via.placeholder.com/150'},],
      stats: {likes: 0, ratings: [1, 1, 14, 61, 1, 1, 1, 1, 1, 150]},
      meta: {
        platforms: 'Windows, Linux, Mac',
        releaseYear: '2021',
        genres: 'Action, Adventure',
        developer: 'Ubisoft',
        publisher: 'Ubisoft',
      }
    }
);
// TODO: remove placeholder data
header.setContent({
  component: gamePageHeader,
  props: {
    id: game.value.id,
    title: game.value.title,
    description: game.value.description,
    image: game.value.image,
  }
})

// TODO: remove placeholder data
const totalRatings = ref(game.value.stats.ratings.reduce((acc, curr) => acc + curr, 0));
const error = ref<string | null>(null);

const api = new BackendApiService()

onMounted(async () => {
  header.setExpanded(true);
  header.setLoading(true);

  try {
    game.value = await api.getGame(gameID);
    totalRatings.value = game.value.stats.ratings.reduce((acc, curr) => acc + curr, 0);

    header.setContent({
      component: gamePageHeader,
      props: {
        id: game.value.id,
        title: game.value.title,
        description: game.value.description,
        image: game.value.image,
      }
    })
  } catch (e) {
    error.value = e.message;
  } finally {
    header.setLoading(false);
  }
});


onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(() => null)
})

</script>

<template>
  <div class="page" v-if="game">
    <div class="content">
      <section class="external-links">
        <!--   list of external links related to the game     -->
        <!--  wikipedia, epic games, gog, ubisoft, steam      -->
        <ExternalLinkItem v-for="link in game.externalLinks" :key="link.url" :url="link.url" :img_url="link.img_url"/>

      </section>
      <section class="related">
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
      <section>
        <h2>Achievements</h2>
        <ul>
          <AchievementItem id="1" title="Mamt" description="Sort"/>
          <AchievementItem id="1" title="Mamt" description="Sort"/>
          <AchievementItem id="1" title="Mamt" description="Sort"/>
        </ul>
      </section>

      <divider></divider>

      <!--   stats is a grid that contains "widgets" - div that are N cols of width and that have rounded corners and dark background   -->
      <div class="stats">
        <div class="widget ratings">
          <ul>
            <li v-for="number in Array.from({length: 10}, (_, i) => i + 1)"
                :style="{ '--percentage': `${game.stats.ratings[number-1] / totalRatings * 100}%` }">
              <span>{{ number }}</span> <span>{{
                Math.round(game.stats.ratings[number - 1] / totalRatings * 100)
              }}%</span>
            </li>
          </ul>
        </div>
      </div>

    </div>
    <div class="metadata">
      <!--   platforms, release year, genres, publisher, developer   -->
      <div class="meta">
        <span class="name">Average Rating</span>
        <span class="value">{{
            (game.stats.ratings.reduce((acc, curr, i) => acc + curr * (i + 1), 0) / totalRatings).toFixed(2)
          }}</span>
      </div>
      <!--   TODO: add more metadata about the game   -->
      <div class="meta" v-for="item in Object.entries(game.meta)" :key="item[0]">
        <span class="name">{{ item[0].capitalize() }}</span>
        <span class="value">{{ item[1] }}</span>
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
        flex-wrap: wrap;
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
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;

      & > .widget {
        border-radius: 6px;
        background: rgba(60, 60, 60, 0.4);
        padding: 6px 10px;

        &.ratings {
          grid-column: span 2;

          & > ul {
            padding: 0;
            margin: 0;
            list-style: none;

            & > li {
              display: flex;

              font-size: .85rem;
              position: relative;

              --percentage: 0%;

              &:not(:last-child) {
                margin-bottom: 4px;
              }

              & > span:first-of-type {
                font-size: .7rem;
                display: block;
                width: 26px;
                text-align: center;
                font-weight: bold;
                background: black;

                border-radius: 4px 0 0 4px;

                &:after {
                  content: '';
                  position: absolute;
                  top: 0;
                  left: 26px;

                  display: block;
                  width: calc(var(--percentage) - 26px);
                  height: 100%;
                  background: rgba(0, 124, 0, 0.2);

                  border-radius: 0 4px 4px 0;
                }
              }

              & > span:nth-child(2) {
                margin-left: 10px;
                color: rgba(255, 255, 255, 0.7);
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