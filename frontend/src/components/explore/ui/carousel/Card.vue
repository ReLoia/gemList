<script setup lang="ts">

import {ref} from "vue";
import {mdiHeart, mdiStar} from "@mdi/js";
import type {GameModel} from "@/types/common.d";

const props = defineProps<{
  game: GameModel
}>()

const isHovered = ref(false)
const totalRatings = props.game.ratings.reduce((acc, curr) => acc + curr, 0.000001);
</script>

<template>
  <li class="card" @mouseover="isHovered = true" @mouseleave="isHovered = false">
    <div>
      <div class="card-preview">
        <router-link :to="{ name: 'game', params: { id: game.id } }"/>
        <img :src="game.cover_image_url" alt="Game Image"/>
      </div>
      <article class="card-content" v-if="isHovered">
        <h3>{{ game.title }}</h3>
        <!--    TODO: add Infos: add to list button - etc      -->
        <p class="metadata">
          <span class="rating">
            <span>{{
                (game.ratings.reduce((acc, curr, i) => acc + curr * (i + 1), 0.000001) / totalRatings).toFixed(2)
              }}</span>
            <svg-icon type="mdi" :path="mdiStar"/>
          </span>

          <span class="likes">
            <span>{{ game.likes }}</span>
            <svg-icon type="mdi" :path="mdiHeart"/>
          </span>
        </p>
        <p>{{ game.description.length > 100 ? game.description.slice(0, 100) + '...' : game.description }}</p>
      </article>
    </div>
  </li>
</template>

<style scoped>
li.card {
  min-width: 300px;
  height: 150px;
  --outer-radius: 12px;
  --inner-radius: 8px;

  border-radius: var(--outer-radius);
  transition: .4s all;

  box-shadow: 0 17px 24px rgba(0, 0, 0, 0.4);

  & > div {
    width: 100%;
    height: 100%;
    transition: .4s all;
    position: relative;

    & > .card-preview {
      position: relative;
      width: 100%;
      height: 100%;

      & > a {
        display: block;
        width: 100%;
        height: 100%;
        border-radius: var(--outer-radius);

        position: absolute;
      }

      & > img {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: var(--outer-radius);

        transition: .6s border-radius;
      }
    }

    & > .card-content {
      opacity: 0;
      height: 0;
      overflow: hidden;

      width: 100%;
      box-sizing: border-box;
    }
  }

  &:hover {
    min-width: 320px;
    margin: -10px;
    height: 160px;

    z-index: 10;

    & > div {
      & > .card-preview {
        & > img {
          border-bottom-left-radius: 0;
          border-bottom-right-radius: 0;
        }
      }

      & > .card-content {
        display: block;
        height: unset;
        position: absolute;
        opacity: 1;

        background: black;
        padding: 10px;

        transition: opacity .6s;

        border-bottom-left-radius: var(--outer-radius);
        border-bottom-right-radius: var(--outer-radius);

        & > .metadata {
          color: #b3b3b3;
          display: flex;

          gap: 8px;
          margin-top: 2px;
          margin-bottom: 12px;

          & > span {
            display: flex;
            line-height: 22px;
            height: 20px;

            & > svg-icon {
              scale: .65;
            }
          }
        }
      }
    }
  }
}
</style>