<script setup lang="ts">
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

  transition: .4s all;

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

  &:hover {
    transform: scale(1.1);
  }
}
</style>