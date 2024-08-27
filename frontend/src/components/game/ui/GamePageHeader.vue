<script setup>

import {mdiPlusCircle} from '@mdi/js';

const props = defineProps({
  title: String,
  description: String,
  image: String
})

console.log(props.title, props.description, props.image)

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
      <!--   Actions -->
      <button>
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

      width: 200px;
      height: 200px;

      position: relative;
    }
  }

  & > div.actions {
    display: flex;
    flex-direction: row;
    align-items: end;
    gap: 20px;
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

      &:hover {
        filter: brightness(.7);
      }
    }
  }
}
</style>