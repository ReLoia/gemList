<script setup>

import '@jamescoyle/svg-icon'
import {mdiMenu, mdiClose, mdiMagnify, mdiCog} from "@mdi/js";

import {onMounted, ref, watch} from "vue";

import {useUserStore} from "@/store/user.js";
import {useHeaderStore} from "@/store/header.js";
import LoadingBar from "@/components/common/LoadingBar.vue";

import {useRouter} from "vue-router";

const router = useRouter();

const user = useUserStore()
const headerStore = useHeaderStore()

const searchState = ref(false)
const menuState = ref(false)

const headerEl = ref(null)
const mainEl = ref(null)
const footerEl = ref(null)

function calculateMainHeight(setHeaderHeight) {
//   calculate the main height and put it in CSS
//   100svh - header height - footer height
  /** @type {HTMLElement} */
  const mainElement = mainEl.value;
  if (!mainElement) return;
  if (setHeaderHeight) {
    mainElement.style.minHeight = `calc(100vh - ${setHeaderHeight}px)`
  } else {
    /** @type {HTMLElement} */
    const headerElement = headerEl.value
    mainElement.style.minHeight = `calc(100vh - ${headerElement.clientHeight}px)`
  }
}

watch(headerStore, (newHeader, _) => {
  const expanded = newHeader.expanded
  calculateMainHeight(expanded ? 340 : 80)
})

onMounted(calculateMainHeight)

</script>

<template>
  <LoadingBar v-if="headerStore.loading"/>
  <header :class="{ expanded: headerStore.expanded, menuOpen: menuState }" ref="headerEl"
          :style="{'--backgroundImage': headerStore.backgroundImage}">
    <div class="content">
      <!--      {{  Open-Close burger button   }}-->
      <button class="has-icon" style="scale: 1.7;" @click="menuState = !menuState">
        <svg-icon v-if="!menuState" type="mdi" :path="mdiMenu"/>
        <svg-icon v-else type="mdi" :path="mdiClose"/>
      </button>
      <!--      {{  Center Title   }}-->
      <router-link to="/" class="title">gemList</router-link>
      <!--      {{  Search and Profile buttons   }}-->
      <div>
        <div class="search" :class="{ expanded: searchState }">
          <input type="text" placeholder="Search anything" id="search" ref="search"/>
          <button class="has-icon" style="scale: 1.4;" @click="e => {
            if (!searchState) searchState = true
            else {
              const searchValue = $refs.search.value

              console.log(searchValue)
            }
          }">
            <svg-icon type="mdi" :path="mdiMagnify"/>
          </button>
        </div>
        <button class="user" :title="user.username || 'Login'" @click="(() => {
          if (user.username) {
            router.push('/profile')
          } else {
            router.push('/login')
          }
        })">
          <img :src="user.avatar || ''" alt="User Avatar"/>
          <svg-icon type="mdi" :path="mdiCog"/>
        </button>
      </div>
    </div>
    <component :is="headerStore.content.component" v-if="headerStore.expanded" v-bind="headerStore.content.props"/>
  </header>
  <left-menu :class="{ expanded: menuState }">
    <router-link to="/">gemList</router-link>
    <router-link to="/">Home</router-link>
    <router-link to="/explore">Explore</router-link>
    <router-link to="/calendar">Calendar</router-link>
    <divider/>
    <router-link to="/library">Library</router-link>
    <router-link to="/community">Community</router-link>
    <router-link to="/friends">Friends</router-link>
  </left-menu>
  <main ref="mainEl">
    <router-view/>
  </main>
</template>

<style scoped>
header {
  background-color: rgba(217, 217, 217, 0.12);
  color: #000;

  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;

  display: flex;
  flex-direction: column;

  position: relative;
  z-index: 1;

  min-height: 80px;

  transition: .8s all;

  & > .content {
    height: 80px;
    box-sizing: border-box;

    position: relative;

    padding: 1rem 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 80px;

    z-index: 1;

    @media (max-width: 768px) {
      padding: 1rem 1rem;
    }

    & > .title {
      font-weight: bold;
      letter-spacing: 4px;
      margin-right: -56px;
    }

    & > div {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 18px;
      position: relative;

      button {
        border-radius: 50%;
      }

      & > div.search {
        display: flex;
        align-items: center;
        position: absolute;
        left: calc(-33px - 40px);

        & > input {
          display: none;
        }

        padding: 8px;
        margin-right: -8px;

        @media (max-width: 768px) {
          display: none;
        }

        &.expanded {
          background: #2F1212;
          width: 260px;
          box-sizing: border-box;
          left: calc(-260px - 40px + 7px);
          border-radius: 8px;
          padding-block: 0;

          & > input {
            display: block;
            width: 100%;
            padding: 8px;
            border: none;
            border-radius: 8px;

            background: none;

            outline: none;
          }

          & > button {
            color: rgba(217, 217, 217, 0.24);
          }
        }
      }

      & > .user {
        width: 34px;
        height: 34px;
        position: relative;

        & > img {
          border-radius: 50%;
          width: 34px;
          height: 34px;
        }

        & > svg-icon {
          position: absolute;
          top: 100%;
          left: 100%;
          transform: translate(-60%, -60%) scale(.62);

          width: 22px;
          height: 22px;

          background: rgba(0, 0, 0, 0.9);
          padding: 5px;
          border-radius: 50%;
        }
        
      }
    }
  }

  &.menuOpen {
    transition: .2s border-radius;
    border-bottom-left-radius: 0;
  }

  &.expanded {
    min-height: 340px;

    --backgroundImage: url("https://api.dicebear.com/9.x/adventurer/png?backgroundColor=b6e3f4,c0aede,d1d4f9");
    overflow: hidden;

    color: #fff;

    /* background */
    &:after {
      position: absolute;
      top: 0;
      left: 0;

      width: 100%;
      height: 100%;
      content: '';

      background-color: red;
      background-image: var(--backgroundImage);
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center;
      filter: brightness(0.3) blur(24px);
      transform: scale(1.1);

      z-index: -1;
    }

    & > .content:after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      max-width: 80%;
      height: 1px;
      background-color: #fff;
      z-index: 1;
    }
  }
}

left-menu {
  display: block;

  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;

  width: 100%;
  max-width: 320px;

  height: calc(100% - 80px);
  margin-top: auto;

  background-color: rgba(217, 217, 217, 0.24);
  z-index: 20;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: .8s all;

  backdrop-filter: blur(10px);

  transform: translateX(-100%);

  &.expanded {
    transform: translateX(0);
  }

  &:not(.expanded) {
    & > a:focus {
      position: absolute;
      left: 100%;
      background: rgba(217, 217, 217, 0.24);
      backdrop-filter: blur(20px);

    }
  }

  & > a {
    display: block;
    padding: 1rem 2rem;

    width: 100%;

    text-decoration: none;

    box-sizing: border-box;

    position: relative;

    &:first-of-type {
      text-align: center;
      letter-spacing: 2px;
      font-weight: bold;
      font-size: 1.1rem;

      margin-bottom: 10px;

      &:after {
        content: '';
        display: block;
        width: 60%;
        height: 1px;
        background-color: #000;

        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
      }
    }

    &:not(:first-of-type) {
      transition: .2s all;

      &.router-link-active {
        background-color: #D9D9D9;
        color: #000;
        font-weight: bold;
      }

      &:hover {
        background-color: rgba(0, 0, 0, 0.1);
      }
    }
  }

  & > divider {
    display: block;
    height: 1px;
    width: 60%;
    margin-inline: auto;

    background: black;
  }
}

main {
  overflow: hidden;
  padding-top: 20px;

  box-sizing: border-box;

  &.center {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}


</style>
