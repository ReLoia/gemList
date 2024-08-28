<script setup>
import {useUserStore} from "../../store/user.js";
import {useHeaderStore} from "../../store/header.js";

import LoginBanner from "./ui/LoginBanner.vue";
import ExploreCarousel from "./ui/carousel/ExploreCarousel.vue";

const user = useUserStore()
const header = useHeaderStore()
</script>


<template>
  <LoginBanner v-if="!user.username"/>

  <ExploreCarousel sort="recent" title="Recent Games"/>

  <ExploreCarousel sort="popular" title="Popular Games"/>

</template>

<style scoped>

</style>