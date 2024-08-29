<script setup lang="ts">
import {BackendApiService} from "../../../api/backend";

defineProps<{
  username: string,
  image: string
}>()

const api = new BackendApiService();
api.setToken(localStorage.getItem('access_token') || '');

</script>

<template>
  <div class="header-info">
    <div class="info">
      <img :src="image || 'https://via.placeholder.com/200'" alt="Profile Picture"/>
      <div>
        <h1>{{ username }}</h1>
        <!--        TODO: add more meta -->
        <p>Member since: </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-info {
  width: 80%;
  max-width: 1400px;
  padding-inline: 40px;
  margin-inline: auto;

  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex: 1;

  & > div.info {
    display: flex;
    flex-direction: row;
    align-items: end;
    padding-bottom: 20px;
    gap: 20px;

    & > img {
      display: block;

      width: 200px;
      height: 200px;
      margin-bottom: 20px;
      margin-left: -50px;

      object-fit: cover;
      object-position: 10%;
      border-radius: 8px;

      position: relative;
    }
  }
}

</style>