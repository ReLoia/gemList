<script setup>
import {useUserStore} from '@/store/user'
import {useHeaderStore} from '@/store/header'

import LoginBanner from "./ui/LoginBanner.vue";
import ExploreItem from "./ui/ExploreItem.vue";

const user = useUserStore()
const header = useHeaderStore()

// TODO: remove this when the backend is ready
let games = [
  {
    id: '1',
    title: 'The Witcher 3: Wild Hunt',
    image: 'https://upload.wikimedia.org/wikipedia/en/0/0c/The_Witcher_3_cover_art.jpg',
    description: 'The Witcher 3: Wild Hunt is a 2015 action role-playing game developed and published by CD Projekt. Based on The Witcher series of fantasy novels by Andrzej Sapkowski, it is the sequel to the 2011 game The Witcher 2: Assassins of Kings. Played in an open world with a third-person perspective, players control protagonist Geralt of Rivia, a monster hunter known as a witcher, who is looking for his missing adopted daughter on the run from the Wild Hunt: an otherworldly force determined to capture and use her powers.',
  }
]

</script>


<template>
  <LoginBanner v-if="!user.username"/>

  <section class="carousel" data-type="reviews">
    <span class="carousel-title">Recent Games</span>
    <div class="container">
      <ExploreItem v-for="game in games" :key="game.id" :game="game"/>
    </div>
  </section>
</template>

<style scoped>
.carousel {
  & > span {
    font-size: 1.3rem;
    font-weight: bold;
    margin-block: 16px;
    margin-left: 60px;
  }

  & > .container {
    display: flex;
    flex-direction: row;
    align-items: flex-end;
    overflow: hidden;

    gap: 20px;
  }
}

</style>