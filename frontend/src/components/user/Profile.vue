<script setup lang="ts">
import ProfilePageHeader from "./ui/ProfilePageHeader.vue";
import {onMounted, onUnmounted, shallowRef} from "vue";
import {useHeaderStore} from "../../store/header";
import {useUserStore} from "../../store/user";

const profilePageHeader = shallowRef(ProfilePageHeader)
const header = useHeaderStore()
const user = useUserStore()


onMounted(() => {
  header.setExpanded(true)
  header.setContent({
    component: profilePageHeader,
    props: {
      username: user.username,
      image: user.avatar
    }
  });
  header.setBackgroundImage(`url(${user.avatar})`);
})

onUnmounted(() => {
  header.setExpanded(false)
  header.setContent(() => null)
  header.setBackgroundImage('')
})

</script>

<template>

</template>

<style scoped>

</style>