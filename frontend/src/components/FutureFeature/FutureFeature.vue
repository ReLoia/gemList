<template>
  <div>
    <h1>FutureFeature</h1>
    <span>this page is or is part of a future feature</span>
    <a href="https://github.com/ReLoia/gemList/">please check on github</a>
    <a href="https://discord.gg/WHBj6Ejx">or on Discord</a>
  </div>
</template>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

h1 {
  margin-top: 2rem;
  font-size: 6rem;
}

span {
  font-size: 1.6rem;
  text-align: center;
}

@media (max-width: 768px) {
  h1 {
    font-size: 3rem;
  }

  span {
    font-size: 1.4rem;
  }
}
</style>