<script setup>

</script>

<template>
  <div class="login-banner">
    <h3>Track, Share and Review your favorite games</h3>
    <p>Have you ever wanted to share the games you've played, track them, write reviews, embed them on other websites, and let others know if you've completed them 100%, how many hours you've played, and more?</p>
    <p><b>Then you'll love Gemlist!</b></p>
    <div>
      <a href="https://github.com/ReLoia/gemList/" class="button">Follow the Development</a>
      <a href="https://discord.gg/WHBj6Ejx" class="button">Share your thoughts on Discord</a>
    </div>
  </div>
</template>

<style scoped>
.login-banner {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;

  width: fit-content;
  max-width: min(94vw, 1000px);
  padding: 16px 12px;
  border-radius: 12px;
  background: rgba(217, 217, 217, 0.12);

  margin-inline: auto;
  margin-block: 20px;
  margin-bottom: 40px;

  & > h3 {
    font-size: 1.7rem;
    font-weight: bold;
    margin-bottom: 8px;
  }

  & > p {
    font-size: 1rem;
    margin-bottom: 6px;
  }

  & > div {
    display: flex;
    flex-direction: row;
    gap: 8px;
    margin-top: 24px;

    & > .button {
      padding: 4px 38px;
      border-radius: 8px;

      font-weight: bold;
      background: var(--primary);
    }
  }
}

</style>