<script setup lang="ts">
import GamePageHeader from "./ui/GamePageHeader.vue";
import {useHeaderStore} from "@/store/header";
import {onMounted, onUnmounted, ref, shallowRef} from "vue";
import {useRoute, useRouter} from "vue-router";
import type {GameModel} from "@/types/common.d";
import ExternalLinkItem from "./ui/ExternalLinkItem.vue";
import SmallGameCard from "@/components/common/SmallGameCard.vue";
import StaffCard from "./ui/StaffCard.vue";
import AchievementItem from "./ui/AchievementItem.vue";
import RatingGraph from "./ui/ReviewsGraph.vue";
import {BackendApiService} from "@/api/backend";

const gamePageHeader = shallowRef(GamePageHeader)
const route = useRoute()
const router = useRouter()
const header = useHeaderStore()

const gameID: string = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id;

const game = ref<GameModel>();
const ratings = ref([]);

const totalRatings = ref();
const error = ref<string | null>(null);

const api = new BackendApiService()

function getAverageRating(ratings) {
  let totalVotes = 0;
  let weightedSum = 0;

  if (!ratings.forEach) return
  
  ratings.forEach((count, index) => {
    let rating = index + 1;
    weightedSum += rating * count;
    totalVotes += count;
  });

  return totalVotes > 0 ? (weightedSum / totalVotes).toFixed(2) : 0;
}

onMounted(async () => {
  header.setExpanded(true);
  header.setLoading(true);

  try {
    game.value = await api.getGame(gameID);
    // totalRatings.value = game.value.ratings.reduce((acc, curr) => acc + curr, 0.000001);
    ratings.value = game.value.ratings

    header.setContent({
      component: gamePageHeader,
      props: {
        id: game.value.id,
        title: game.value.title,
        description: game.value.description,
        image: game.value.cover_image_url,
      }
    })
    header.setBackgroundImage(`url(${game.value.cover_image_url})`);
  } catch (e) {
    if (e.message) return router.push({name: '404'});
    error.value = e.message;
  } finally {
    header.setLoading(false);
  }
});


onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(() => null)
  header.setBackgroundImage('')
})

</script>

<template>
  <div class="page" v-if="game">
    <div class="content">
      <section class="external-links">
        <!--   list of external links related to the game     -->
        <!--  wikipedia, epic games, gog, ubisoft, steam      -->
        <ExternalLinkItem v-for="link in game.external_links" :key="link.url" :url="link.url" :img_url="link.img_url"/>
      </section>
      <div class="meta">
        <div class="meta-info">
          <h2 v-auto-resize>{{ game.likes.toShortString() }}</h2>
          <p>Likes</p>
        </div>
        <div class="meta-info">
          <h2 v-auto-resize>{{ getAverageRating(ratings) }}</h2>
          <p>Rating</p>
        </div>
        <RatingGraph :ratings="ratings" :game_id="game.id" @update-ratings="r => { ratings = r }" />
      </div>
      <div class="game-info">
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
        <section class="related">
          <h2>Related Games</h2>
          <ul>
            <!--          TODO: load related games from backend -->
            <!-- TODO: add see more button -->
            <SmallGameCard v-for="i of Array(1)" :id="String(i)" img_url="https://via.placeholder.com/150"/>
          </ul>
        </section>
        <section>
          <h2>from the Same Publisher</h2>
          <ul>
            <SmallGameCard id="1" img_url="https://via.placeholder.com/150"/>
          </ul>
        </section>
      </div>
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
          Ratings
          <ul>
            <li v-for="number in Array.from({length: 10}, (_, i) => i + 1)"

                :style="{ '--percentage': `${game.ratings[number-1] / totalRatings * 100}%` }">
              <span>{{ number }}</span> <span>{{
                Math.round(game.ratings[number - 1] / totalRatings * 100)
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
            (game.ratings.reduce((acc, curr, i) => acc + curr * (i + 1), 0.000001) / totalRatings).toFixed(2)
          }}</span>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 5px;

  width: 96%;
  height: 100%;
  max-width: 1200px;
  margin: auto auto 200px;

  padding-inline: 15px;

  & > .content {
    & > .meta {
      display: flex;
      flex-direction: row;
      
      width: 100%;
      max-width: min(98%, 900px);
      height: 90px;
      
      background: #4e2f2f;
      border-radius: 12px;
      
      margin-inline: auto;
      margin-top: 30px;
      
      & > .meta-info {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        overflow-x: auto;
        
        width: 90px;
        position: relative;
        
        padding-inline: 10px;
        
        & > h2 {
          font-size: 2.4rem;
          color: #fff;
        }
        
        & > p {
          color: #909090;
          font-size: .9rem;
          
          position: absolute;
          bottom: 14px;
        }
      }
      
    }
    
    & > .game-info {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;

      & > section {
        &:first-child {
          grid-column: span 2;
          & > h2 {
            margin-left: 20px;
            text-align: start;
          }
        }

        & > h2 {
          text-align: center;
        }
      }
    }


    & section {
      & > h2 {
        //margin-left: 20px;
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
