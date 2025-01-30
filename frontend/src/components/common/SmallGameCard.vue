<script setup lang="ts">
defineProps<{
  id: string,
  img_url: string,
}>()
</script>

<template>
  <li class="card">
    <div class="card-preview">
      <RouterLink :to="{name: 'game', params: {id: id}}"/>
      <img :src="img_url" alt="Game Image"/>
    </div>
  </li>
</template>

<style scoped>
.card {
  min-width: 150px;
  height: 75px;
  --outer-radius: 12px;
  --inner-radius: 8px;

  border-radius: var(--outer-radius);
  transition: .4s all;

  & > .card-preview {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
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

    &:hover {
      transform: scale(1.1);
    }
  }
}
</style>