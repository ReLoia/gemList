<script setup lang="ts">
import {onMounted, onUnmounted, ref} from "vue";
import {APIError, BackendApiService} from "@/api/backend";
import {useRouter} from "vue-router";

const api = new BackendApiService()
const router = useRouter()

const error = ref("");

let redirect = new URLSearchParams(location.search).get('redirect')

async function login(event: SubmitEvent) {
  event.preventDefault()

  if (!event.target) return;
  
  const username = event.target["username"].value
  const password = event.target["password"].value

  try {
    const result = await api.login(username, password);
    
    if (result.access_token) {
      localStorage.setItem('access_token', result.access_token)
      if (redirect?.startsWith("http"))
        redirect = "/";
      await router.push(redirect || '/')
    }
  } catch (e) {
    if (e instanceof APIError)
      error.value = e.message
    else
      console.error(e, e.message)
  }
}

onMounted(() => {
  document.querySelector('main').classList.add('center')
})

onUnmounted(() => {
  document.querySelector('main').classList.remove('center')
})

</script>

<template>
  <div class="card">
    <section class="infos">
      <h2>Login</h2>

      <p>Access your account and continue tracking and rating your games! <br> <br> Rate games, write reviews and more!
        <br>
        <b class="error">{{ error }}</b>
      </p>

      <p class="register">Don't have an account?
        <router-link to="/register">Register</router-link>
      </p>

    </section>
    <form class="form" @submit="login">
      <div class="param">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>
      </div>
      <div class="param">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<style scoped>
div.card {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  width: 880px;
  height: 520px;
  margin-top: -120px;

  border-radius: 12px;

  background: #4e2f2f;
  color: white;

  box-shadow: 0 10px 16px rgba(0, 0, 0, 0.6);

  overflow: hidden;

  @media (max-width: 768px) {
    flex-direction: column;
    max-width: 97vw;

    & form {
      border-left: none !important;
      border-top: 1px solid #e0e0e0;

      padding-block: 20px !important;
    }
  }

  & > * {
    width: 100%;
    height: 100%;

    &.infos {
      display: flex;
      flex-direction: column;
      justify-content: space-between;

      & > h2 {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 10px;
        margin-inline: auto;
        width: fit-content;
      }

      & > p:not(.register) {
        font-size: 1.15rem;
        max-width: 300px;

        & > .error {
          color: red;
          min-height: 1ch;
          display: block;
          margin-top: 10px;
        }
      }
      
      & > .register > a {
        color: #0077cc;
        font-weight: bold;
        text-decoration: none;
        cursor: pointer;
      }

      padding: 20px;
    }

    &.form {
      padding: 20px;
      border-left: 1px solid #e0e0e0;

      display: flex;
      flex-direction: column;

      padding-block: 60px;

      & > .param {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;

        & > label {
          margin-left: 6px;
          font-size: .9rem;

          margin-bottom: 5px;
        }

        & > input {
          padding: 8px 6px;
          border: 1px solid #d0d0d0;
          border-radius: 8px;
          font-size: 1.1rem;
        }
      }

      & > button {
        margin-top: auto;
        margin-inline: auto;
        padding: 8px 20px;
        border: none;
        border-radius: 8px;

        background: #0077cc;
        color: white;

        font-size: 1.1rem;
        font-weight: bold;

        min-width: 200px;

        cursor: pointer;
        transition: filter .2s;

        &:hover {
          filter: brightness(.7);
        }
      }
    }
  }
}
</style>