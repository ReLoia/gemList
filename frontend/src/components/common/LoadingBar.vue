<script setup>

</script>

<template>
  <div class="bar">

  </div>
</template>

<style scoped>
div.bar {
  position: absolute;
  top: 0;
  z-index: 200;

  height: 4px;
  width: 100%;

  &:after {
    content: '';
    display: block;
    width: 200px;
    height: 100%;
    background-color: #f0f0f0;

    position: relative;

    animation: loading 4s infinite ease-in-out;
  }
}

@keyframes loading {
  0% {
    left: 0;
  }
  50% {
    left: calc(100% - 200px);
  }
  100% {
    left: 0;
  }
}

</style>