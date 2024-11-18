import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Noticias from '../views/Noticias.vue';
import Contacto from '../views/Contacto.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/noticias',
    name: 'Noticias',
    component: Noticias
  },
  {
    path: '/contacto',
    name: 'Contacto',
    component: Contacto
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
