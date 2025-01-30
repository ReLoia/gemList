<script setup lang="ts">
import {mdiTrophy} from "@mdi/js";

defineProps<{
  id: string,
  // img_url: string,
  title: string,
  description: string
}>()
</script>

<template>
  <li class="card">
    <RouterLink :to="{name: 'achievement', params: {id: id}}"/>
    <div class="card-preview">
      <svg-icon type="mdi" :path="mdiTrophy"/>
    </div>
    <div class="card-content">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
    </div>
  </li>
</template>

<style scoped>
li.card {
  position: relative;

  width: fit-content;
  min-width: 300px;
  height: 80px;

  --outer-radius: 40px;
  --inner-radius: 8px;

  border-radius: var(--outer-radius);
  overflow: hidden;

  background: burlywood;

  display: flex;
  align-items: center;
  gap: 10px;

  & > a {
    width: 100%;
    height: 100%;
    position: absolute;
    display: block;
  }

  & > .card-preview {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 5px;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: black;
    color: white;
    font-size: 1.5rem;

    & > svg-icon {
      height: 26px;
    }
  }

  & > .card-content {
    color: black;

    & > h3 {
      line-height: .8;
    }
  }
}
</style>