import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    name: 'home',
    strict: true,
    components: {
      default: () => import('./DashboardApp.vue'),
    },
  },
];

export default routes;
