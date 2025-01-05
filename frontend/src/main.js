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
    {path: '/', component: () => import('./components/FutureFeature/FutureFeature.vue'), meta: {title: 'Home'}},
    {path: '/explore', component: () => import('./components/explore/Explore.vue'), meta: {title: 'Explore'}},
    {path: '/game/:id', component: () => import('./components/game/Game.vue')},

    {path: '/login', component: () => import('./components/user/Login.vue'), meta: {title: 'Login'}},
    {path: '/register', component: () => import('./components/user/Register.vue'), meta: {title: 'Register'}},
    {path: '/profile', component: () => import('./components/user/profile/Profile.vue'), meta: {requiresAuth: true}},
    {path: '/user/:id', component: () => import('./components/user/User.vue')},

    //     TODO: change the path to the correct components
    {path: '/staff/:id', component: () => import('./components/FutureFeature/FutureFeature.vue')},
    {path: '/achievement/:id', component: () => import('./components/FutureFeature/FutureFeature.vue')},

    {path: '/calendar', component: () => import('./components/FutureFeature/FutureFeature.vue')},
    {path: '/library', component: () => import('./components/FutureFeature/FutureFeature.vue')},
    {path: '/community', component: () => import('./components/FutureFeature/FutureFeature.vue')},
    {path: '/friends', component: () => import('./components/FutureFeature/FutureFeature.vue')},

    {path: '/:pathMatch(.*)*', component: () => import('./components/404/NotFound.vue')},
].map(route => {
    if (route.name === undefined) {
        route.name = route.path.split('/')[1]
    }
    return route
});

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    scrollBehavior: () => ({y: 0}),
    routes,
});

const pinia = createPinia()
const app = createApp(App)
    .use(pinia);

router.beforeEach(async (to, from, next) => {
    let changed = true;
    
    const token = localStorage.getItem('access_token')
    const userIsLogged = token !== null && token !== "";

    const userStore = useUserStore();

    if (to.matched.some(record => record.meta.requiresAuth) && !userIsLogged) {
        next('/login?redirect=' + to.fullPath)
        return;
    }

    if (to.path === '/' && !userIsLogged) {
        next('/explore')
        changed = false;
    } else {
        await userStore.loadUser(token)
        next()
    }

    if (changed && to.meta.title) {
        document.title = to.meta.title + ' - gemList'
    } else {
        document.title = 'gemList'
    }
});


app
    .use(router)
    .mount("#app");

history.scrollRestoration = 'manual';
