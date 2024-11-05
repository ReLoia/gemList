<script setup lang="ts">
import ProfilePageHeader from "./ProfilePageHeader.vue";
import {onMounted, onUnmounted, shallowRef} from "vue";
import {useHeaderStore} from "../../../store/header";
import {useUserStore} from "../../../store/user";
import Carousel from "./ui/Carousel.vue";

const profilePageHeader = shallowRef(ProfilePageHeader)
const header = useHeaderStore()
const user = useUserStore()

onMounted(() => {
  header.setExpanded(true)
  header.setContent({
    component: profilePageHeader,
    props: {
      username: user.username,
      image: user.avatar,
      creation_date: user.creation_date
    }
  });
  header.setBackgroundImage(`url(${user.avatar})`);
})

onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(() => null)
  header.setBackgroundImage('')
})

</script>

<template>
  <div class="page">
    <div class="content">
      <Carousel title="Games Played" :items="user.games_played"/>
      <Carousel title="Games Liked" :items="user.games_liked"/>
      <Carousel title="Games Rated" :items="user.games_rated"/>
      <Carousel title="Reviews" :items="[]"/>
    </div>
    <!--    TODO: add metadata -->
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
  margin: auto auto 200px;

  padding-inline: 15px;


  & > .content {
    grid-area: content;


    & > divider {
      display: block;
      height: 1px;
      margin-block: 30px;
      width: 90%;
      margin-inline: auto;

      background: white;
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