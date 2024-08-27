import {createApp} from 'vue'
import {createPinia, storeToRefs} from 'pinia'
import {useUserStore} from "./store/user.js";

import './style.css'
import App from './App.vue'
import {createRouter, createWebHistory} from 'vue-router'

String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

const routes = [
    {path: '/', component: () => import('./components/home/Home.vue')},
    {path: '/explore', component: () => import('./components/explore/Explore.vue')},
    {path: '/game/:id', component: () => import('./components/game/Game.vue')},

    //     TODO: change the path to the correct components
    {path: '/staff/:id', component: () => import('./components/404/NotFound.vue')},
    {path: '/achievement/:id', component: () => import('./components/404/NotFound.vue')},

    {path: '/calendar', component: () => import('./components/404/NotFound.vue')},
    {path: '/library', component: () => import('./components/404/NotFound.vue')},
    {path: '/community', component: () => import('./components/404/NotFound.vue')},
    {path: '/friends', component: () => import('./components/404/NotFound.vue')},

    {path: '/login', component: () => import('./components/404/NotFound.vue')},
    {path: '/register', component: () => import('./components/404/NotFound.vue')},
    {path: '/profile', component: () => import('./components/404/NotFound.vue')},

    {path: '/:pathMatch(.*)*', component: () => import('./components/404/NotFound.vue')},
].map(route => {
    if (route.name === undefined) {
        route.name = route.path.split('/')[1]
    }
    return route
});

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const pinia = createPinia()
const app = createApp(App)
    .use(pinia);
const userStore = useUserStore()
const {username} = storeToRefs(userStore)

router.beforeEach((to, from, next) => {
    const userIsLogged = username.value !== '';
    if (to.path === '/' && !userIsLogged) {
        next('/explore')
    } else {
        next()
    }
});


app
    .use(router)
    .mount("#app");

history.scrollRestoration = 'manual';
