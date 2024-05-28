import { createRouter, createWebHistory } from "vue-router";

import simpleRoute from '../modules/simpleModule/routes'
import Test from '../modules/simpleModule/Module.vue';

const routes = [
    // {
    //     path: '/',
    //     component:  home
    // }

    {
        path: '/test',
        component: Test
    }
];

routes.push(simpleRoute)

const router = new createRouter({
    routes,
    history: createWebHistory()
});

export default router;