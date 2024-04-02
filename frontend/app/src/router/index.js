import home from '../pages/home.vue'
import { createRouter, createWebHistory } from "vue-router";

import simpleRoute from '../modules/simpleModule/routes'

const routes = [
    {
        path: '/',
        component:  home
    }
];

routes.push(simpleRoute)

const router = new createRouter({
    routes,
    history: createWebHistory()
});

export default router;