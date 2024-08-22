<script setup lang="ts">
import {mdiChevronLeft, mdiChevronRight} from "@mdi/js";
import Card from "./Card.vue";

const props = defineProps<{
  items: any[],
  title: string
}>()

function scrollCarousel(direction: 'left' | 'right') {
  const carousel = document.querySelector('.carousel[data-type="reviews"] .container') as HTMLElement
  const scrollAmount = 200
  const scrollDirection = direction === 'left' ? -1 : 1

  carousel.scrollBy({
    left: scrollAmount * scrollDirection,
    behavior: 'smooth'
  })
}

</script>

<template>
  <section class="carousel" data-type="reviews">
    <span class="carousel-title">{{ title }}</span>
    <div class="container">
      <button @click="scrollCarousel('left')">
        <svg-icon type="mdi" :path="mdiChevronLeft" :size="1.5"/>
      </button>
      <ul>
        <Card v-for="item in items" :key="item.id" :game="item"/>
      </ul>
      <button @click="scrollCarousel('right')">
        <svg-icon type="mdi" :path="mdiChevronRight"/>
      </button>
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

    position: relative;

    & > button {
      position: absolute;
      top: 50%;
      transform: translateY(calc(-50% / 2.4));
      --horizontal-spacing: 8px;

      opacity: 0;
      scale: 2.4;

      height: calc(140px / 2.4);

      transition: opacity 0.6s;

      left: var(--horizontal-spacing);

      &:last-of-type {
        left: unset;
        right: var(--horizontal-spacing);
      }
    }

    &:hover > button {
      opacity: 1;
    }

    & > ul {
      display: flex;
      align-items: flex-start;
      list-style: none;
      gap: 20px;

      overflow-x: scroll;
      -webkit-scroll-snap-type: x proximity;
      scroll-snap-type: x proximity;
      scroll-behavior: smooth;
      scrollbar-width: none;
    }
  }
}

</style>