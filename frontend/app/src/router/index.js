import { createRouter, createWebHistory } from "vue-router";

import simpleRoute from '../modules/simpleModule/routes'
import recomendedFilmRoute from '../modules/recomendedFilm/routes.js'
import recomendedPhoneRoute from '../modules/recomendedPhone/routes.js'


const routes = [];

// подключение маршрутов модулей
routes.push(simpleRoute)
routes.push(...recomendedFilmRoute)
routes.push(...recomendedPhoneRoute)

const router = new createRouter({
    routes,
    history: createWebHistory()
});

export default router;