<script setup lang="ts">

interface Game {
  id: string
  title: string
  image: string
  description: string
}

defineProps<{
  game: Game
}>()

</script>

<template>
  <li class="card">
    <div>
      <div class="card-preview">
        <router-link :to="'/game/' + game.id"/>
        <img :src="game.image" alt="Game Image"/>
      </div>
      <article class="card-content">
        <h3>{{ game.title }}</h3>
        <!--    TODO: add Infos: likes - rating - add to list button - etc      -->
        <p class="metadata">
          <span class="likes">
            <svg-icon type="mdi" :path="mdiHeartOutline"/>
            <span>{{ game.likes }}</span>
          </span>
        </p>
        <p>{{ game.description.length > 100 ? game.description.slice(0, 100) + '...' : game.description }}</p>
      </article>
    </div>
  </li>
</template>

<style scoped>
li.card {
  min-width: 280px;
  height: 140px;
  --outer-radius: 12px;
  --inner-radius: 8px;

  border-radius: var(--outer-radius);
  transition: .4s all;

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

        background: red;
      }
    }

    & > .card-content {
      opacity: 0;
      height: 0;
      overflow: hidden;

    }
  }

  &:hover {
    margin: -10px;
    min-width: 300px;
    height: 150px;

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

        & > p {
          margin-top: 4px;
        }
      }


    }
  }
}
</style>