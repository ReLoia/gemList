<script setup lang="ts">
import {BackendApiService} from "@/api/backend";
import {mdiCog} from "@mdi/js";

defineProps<{
  username: string,
  image: string,
  creation_date: string
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
        <p>Member since: {{ new Date(creation_date).toLocaleDateString() }}</p>
      </div>
    </div>
    <div class="actions">
      <router-link to="/settings">
        <svg-icon type="mdi" :path="mdiCog"/>
        Settings
      </router-link>
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

    & > :is(a, button) {
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

      &:hover {
        filter: brightness(.7);
      }
    }
  }

  @media (max-width: 700px) {
    padding-top: 40px;
    flex-direction: column;
  }

  @media (max-width: 800px) {
    width: 90%;
  }

  @media (max-width: 500px) {
    padding-inline: 10px;
    & > div.info {
      flex-direction: column;
      align-items: start;

      & > img {
        margin-left: 0;
        margin-bottom: 0;
      }
    }
  }
}

</style>