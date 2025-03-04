<script setup lang="ts">
import {mdiChevronLeft, mdiChevronRight} from "@mdi/js";
import Card from "./Card.vue";
import {onMounted, ref} from "vue";
import {BackendApiService} from "@/api/backend";

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

const items = ref([]);
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
  <section class="carousel">
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

      @media (max-width: 600px) {
        padding-inline: 14px 300px;
      }

    }
  }
}
</style>