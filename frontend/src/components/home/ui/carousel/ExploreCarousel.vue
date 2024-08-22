<script setup lang="ts">
import {mdiChevronLeft, mdiChevronRight} from "@mdi/js";
import Card from "./Card.vue";
import {ref} from "vue";

const props = defineProps<{
  items: any[],
  title: string
}>()

const carousel = ref(null)

const canScrollLeft = ref(false)
const canScrollRight = ref(true)

let scrollPosition = 0;

function scrollCarousel(direction: 'left' | 'right') {
  const scrollAmount = 300
  const scrollDirection = direction === 'left' ? -1 : 1;

  if (direction === 'left') {
    canScrollRight.value = true
    if ((carousel.value as HTMLUListElement).scrollLeft - scrollAmount <= 0) {
      canScrollLeft.value = false
    }
  } else {
    canScrollLeft.value = true
    if ((carousel.value as HTMLUListElement).scrollLeft + scrollAmount >= (carousel.value as HTMLUListElement).scrollWidth - (carousel.value as HTMLUListElement).clientWidth) {
      canScrollRight.value = false
    }
  }

  scrollPosition = Math.max(0, scrollPosition + scrollAmount * scrollDirection);
  (carousel.value as HTMLUListElement).scrollTo({
    left: scrollPosition,
    behavior: 'smooth'
  })
}

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
  margin-top: 20px;

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

      z-index: 12;

      &:last-of-type {
        left: unset;
        right: var(--horizontal-spacing);
      }

      &.disabled {
        display: none;
      }
    }

    &:hover > button {
      opacity: 1;
    }

    & > ul {
      display: flex;
      list-style: none;
      gap: 20px;

      overflow-x: scroll;
      scroll-behavior: smooth;
      scrollbar-width: none;
      -webkit-scroll-snap-type: x proximity;
      scroll-snap-type: x proximity;

      padding-top: 40px;
      padding-bottom: 300px;

      margin-top: -20px;
      margin-bottom: -280px;

      padding-inline: 80px;
    }
  }
}
</style>