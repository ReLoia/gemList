<script setup lang="ts">

import {defineProps} from 'vue'

defineProps<{
  url: string,
  img_url: string,
}>()

</script>

<template>
  <div class="external-link-item">
    <a :href="url" target="_blank">
      <img :src="img_url" alt="external link"/>
    </a>
  </div>
</template>

<style scoped>
.external-link-item {
  display: inline-block;
  width: 60px;
  height: 60px;
  border-radius: 10px;
  overflow: hidden;

  a {
    display: block;
    width: 100%;
    height: 100%;
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
</style>