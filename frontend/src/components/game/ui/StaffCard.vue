<script setup lang="ts">

import {ref} from "vue";

defineProps<{
  staff: {
    id: string,
    img_url: string,
    name: string
    role: string
  }
}>()

const isHovered = ref(false)

</script>

<template>
  <li class="card" @mouseover="isHovered = true" @mouseleave="isHovered = false">
    <div class="card-preview">
      <RouterLink :to="{name: 'staff', params: {id: staff.id}}"/>
      <img :src="staff.img_url" alt="Author Image"/>
    </div>
    <div class="card-content">
      <h3>{{ staff.name }}</h3>
      <p>{{ staff.role }}</p>
    </div>
  </li>
</template>

<style scoped>
.card {
  min-width: 75px;
  height: 75px;
  --outer-radius: 12px;
  --inner-radius: 8px;

  border-radius: var(--outer-radius);
  transition: .4s all;

  display: flex;

  position: relative;

  & > .card-preview {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 75px;
    height: 75px;
    border-radius: var(--outer-radius);
    overflow: hidden;
    position: relative;
    cursor: pointer;
    transition: .4s all;

    background: #000;

    & > a {
      width: 100%;
      height: 100%;
      position: absolute;
      display: block;
    }

    & > img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .card-content {
    position: absolute;
    left: 100%;

    height: 75px;
    z-index: 10;

    opacity: 0;
    max-width: 0;
    width: fit-content;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    border-radius: 0 var(--inner-radius) var(--inner-radius) 0;
    padding: 0;

    transition: .4s all;

    & > h3 {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  &:hover {


    .card-preview {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
    }

    .card-content {
      opacity: 1;
      padding: 10px;
      max-width: unset;
    }
  }
}

</style>