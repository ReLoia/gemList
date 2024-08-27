<script setup>
import {useUserStore} from "../../store/user.js";
import {useHeaderStore} from "../../store/header.js";

import LoginBanner from "./ui/LoginBanner.vue";
import ExploreCarousel from "./ui/carousel/ExploreCarousel.vue";

const user = useUserStore()
const header = useHeaderStore()

// TODO: remove this when the backend is ready
let games = [
  {
    id: '1',
    title: 'The Witcher 3: Wild Hunt',
    image: 'https://steamcdn-a.akamaihd.net/steam/apps/292030/header.jpg?t=1631046447',
    description: 'The Witcher 3: Wild Hunt is a 2015 action role-playing game developed and published by CD Projekt. Based on The Witcher series of fantasy novels by Andrzej Sapkowski, it is the sequel to the 2011 game The Witcher 2: Assassins of Kings. Played in an open world with a third-person perspective, players control protagonist Geralt of Rivia, a monster hunter known as a witcher, who is looking for his missing adopted daughter on the run from the Wild Hunt: an otherworldly force determined to capture and use her powers.',
    stats: {
      ratings: [11, 12, 63, 42, 514, 14, 63, 244, 11, 3],
      likes: 100
    },
    meta: {
      genres: ""
    },
    externalLinks: [
      {
        img_url: '',
        url: 'https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/'
      }
    ]
  }
];
games[1] = games[0];
games[2] = games[0];
games[3] = games[0];

</script>


<template>
  <LoginBanner v-if="!user.username"/>

  <ExploreCarousel :items="games" title="Top Rated Games"/>

  <ExploreCarousel :items="games" title="Recent Games"/>

  <ExploreCarousel :items="games" title="Popular Games"/>

</template>

<style scoped>

</style>