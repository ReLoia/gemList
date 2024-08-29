<script setup lang="ts">
import {mdiChevronLeft, mdiChevronRight} from "@mdi/js";
import Card from "./Card.vue";
import {onMounted, ref} from "vue";
import {BackendApiService} from "../../../../api/backend";

const props = defineProps<{
  sort: string,
  title: string
}>();
const carousel = ref(null)

const canScrollLeft = ref(false)
const canScrollRight = ref(true)

let scrollPosition = 0;

function scrollCarousel(direction: 'left' | 'right') {
  const scrollAmount = 320
  const scrollDirection = direction === 'left' ? -1 : 1;

  if (direction === 'left') {
    if (!canScrollLeft.value) return

    canScrollRight.value = true
    if ((carousel.value as HTMLUListElement).scrollLeft - scrollAmount <= 0) {
      canScrollLeft.value = false
    }
  } else {
    if (!canScrollRight.value) return

    canScrollLeft.value = true
    if ((carousel.value as HTMLUListElement).scrollLeft + scrollAmount + 300 >= (carousel.value as HTMLUListElement).scrollWidth - (carousel.value as HTMLUListElement).clientWidth) {
      canScrollRight.value = false
    }
  }

  scrollPosition = Math.max(0, scrollPosition + scrollAmount * scrollDirection);
  (carousel.value as HTMLUListElement).scrollTo({
    left: scrollPosition,
    behavior: 'smooth'
  })
}

const api = new BackendApiService();

// TODO: remove placeholder data
const items = ref([
  {
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
  },
  {
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
]);
const loading = ref(true);
const error = ref(false);

const fetchGames = async () => {
  try {
    items.value = await api.getGames(props.sort);
  } catch (e) {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchGames();
})

</script>

<template>
  <section class="carousel" data-type="reviews">
    <span class="carousel-title">{{ title }}</span>
    <div class="container">
      <button @click="scrollCarousel('left')" :class="{ disabled: !canScrollLeft }">
        <svg-icon type="mdi" :path="mdiChevronLeft"/>
      </button>
      <ul v-on:wheel="e => e.preventDefault()" ref="carousel">
        <Card v-for="item in items" :key="item.id" :game="item"/>
      </ul>
      <button @click="scrollCarousel('right')" :class="{ disabled: !canScrollRight }">
        <svg-icon type="mdi" :path="mdiChevronRight"/>
      </button>
    </div>
  </section>
</template>

<style scoped>
.carousel {
  margin-top: 30px;

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

    position: relative;

    & > button {
      position: absolute;
      top: 50%;
      transform: translateY(calc(-50% / 2.4));
      --horizontal-spacing: 18px;
      --horizontal-expand: 10px;

      opacity: 0;
      scale: 2.4;

      height: calc(140px / 2.4);

      transition: opacity 0.6s;

      left: var(--horizontal-spacing);
      padding-right: var(--horizontal-expand);
      border-top-right-radius: 20px;
      border-bottom-right-radius: 20px;

      z-index: 12;

      background: rgba(0, 0, 0, 0.06);
      backdrop-filter: blur(4px);

      &:last-of-type {
        left: unset;
        padding-right: 0;
        right: var(--horizontal-spacing);
        padding-left: var(--horizontal-expand);
        border-radius: 20px 0 0 20px;
      }

      &.disabled {
        opacity: 0;
        cursor: default;
      }
    }

    &:hover > button {
      opacity: 1;
    }

    & > ul {
      display: flex;
      list-style: none;
      gap: 20px;
      min-height: 150px;

      overflow-x: scroll;
      scroll-behavior: smooth;
      scrollbar-width: none;
      -webkit-scroll-snap-type: x proximity;
      scroll-snap-type: x proximity;

      padding-block: 40px 300px;
      padding-inline: 80px 300px;

      margin-top: -20px;
      margin-bottom: -280px;

    }
  }
}
</style>