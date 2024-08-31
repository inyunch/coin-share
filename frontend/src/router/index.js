import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import ManageGroups from '@/components/ManageGroups.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/register', component: Register },
  { path: '/manage-groups', component: ManageGroups },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;