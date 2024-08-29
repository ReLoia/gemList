<script setup lang="ts">
import {mdiPlusCircle, mdiHeartCircle} from '@mdi/js';
import {BackendApiService} from "../../../api/backend";
import {useUserStore} from '../../../store/user';
import {useRouter} from "vue-router";

const router = useRouter()
const user = useUserStore()

const props = defineProps<{
  id: string,
  title: string,
  description: string,
  image: string
}>()

const api = new BackendApiService();
if (user.username) api.setToken(user.token);

function likeGame(id: string) {
  api.likeGame(id)
}

function addGame(id: string) {
  // if the user is not logged in, redirect to login page
  if (!user.username) {
    router.push({name: 'login'})
    return
  }
  // TODO: add game to user list
  // api.addGame(id)
}

</script>

<template>
  <div class="header-info">
    <div class="info">
      <!--   Info about the game   -->
      <img :src="image || 'https://via.placeholder.com/200'" alt="Game Image"/>
      <div>
        <h1>{{ title }}</h1>
        <p>{{ description }}</p>
      </div>
    </div>
    <div class="actions">
      <button class="like" @click="likeGame(id)" v-if="user.username">
        <svg-icon type="mdi" :path="mdiHeartCircle"/>
      </button>
      <button class="add" @click="addGame(id)">
        <svg-icon type="mdi" :path="mdiPlusCircle"/>
        Add
      </button>
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

      width: 250px;
      height: 160px;
      margin-bottom: 20px;
      margin-left: -50px;

      object-fit: cover;
      object-position: 10%;
      border-radius: 8px;

      position: relative;
    }
  }

  & > div.actions {
    display: flex;
    flex-direction: column;
    justify-content: end;
    align-items: end;
    gap: 14px;
    padding-bottom: 20px;

    & > button {
      padding: 4px 20px;
      border-radius: 10px;
      background: #fff;
      color: var(--primary);
      font-weight: bold;
      cursor: pointer;
      transition: .4s all;

      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 6px;
      font-size: 1.1rem;

      & > svg-icon {
        max-height: 24px;
        scale: .9;
      }

      &.like {
        border-radius: 50%;
        padding: 2px;
        width: fit-content;
      }

      &:hover {
        filter: brightness(.7);
      }
    }
  }
}
</style>