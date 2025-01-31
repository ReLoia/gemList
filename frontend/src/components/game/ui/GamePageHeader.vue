<script setup lang="ts">
import {mdiPlusCircle, mdiHeartCircle} from '@mdi/js';
import {BackendApiService} from "@/api/backend";
import {useUserStore} from '@/store/user';
import {useHeaderStore} from "@/store/header";
import {useRouter} from "vue-router";
import {ref} from "vue";

const router = useRouter()
const user = useUserStore()
const header = useHeaderStore()

const props = defineProps<{
  id: string,
  title: string,
  description: string,
  image: string,
  userLiked: boolean
}>()
const uLiked = ref(props.userLiked)

const api = new BackendApiService();
if (localStorage.getItem('access_token'))
  api.setToken(localStorage.getItem('access_token') || '');

async function likeGame(id: string) {
  const res = await api.likeGame(id)
  if (res.message == "Game liked") {
    uLiked.value = true
    header.emit("like", true)
  } else {
    uLiked.value = false
    header.emit("like", false)
  }
}

function addGame(id: string) {
  if (!user.username) {
    router.push({name: 'login?redirect=' + router.currentRoute.value.fullPath})
    return
  }

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
      <button class="like" :class="{ liked: uLiked }" @click="likeGame(id)" v-if="user.username">
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

  @media (max-width: 800px) {
    width: 98%;
    padding-inline: 10px;
  }

  @media (max-width: 500px) {
    padding-top: 40px;
    flex-direction: column;
  }

  & > div.info {
    display: flex;
    flex-direction: row;
    align-items: end;
    padding-bottom: 20px;
    gap: 20px;

    & > div {
      & > h1 {
        font-size: 2.2rem;
        margin-bottom: 3px;
      }

      & > p {
        font-size: .9em;
        color: #EEE;
      }

      margin-bottom: 15px;
    }

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

      @media (max-width: 800px) {
        display: none;
      }
    }

    @media (max-width: 800px) {
      & > div {
        & > h1 {
          font-size: 2rem;
        }

        & > p {
          font-size: 1.05rem;
        }
      }
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

        &.liked {
          background: var(--primary);
          color: #fff;
        }
      }

      &:hover {
        filter: brightness(.7);
      }
    }
  }
}
</style>