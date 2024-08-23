<script setup>


</script>

<template>
  <div class="header-info">
    <div class="info">
      <!--   Info about the game   -->
      <img src="" alt="">
      <div>
        <h1>Game Title</h1>
        <p>Game Description</p>
      </div>
    </div>
    <div class="actions">
      <!--   Actions -->
      <button>
        Add
      </button>
    </div>
  </div>
</template>

<style scoped>
.header-info {
  width: 100%;
  max-width: 1400px;
  padding-inline: 40px;
  margin-inline: auto;

  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex: 1;

  background: rebeccapurple;

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
    align-items: center;
    gap: 20px;
  }
}
</style>