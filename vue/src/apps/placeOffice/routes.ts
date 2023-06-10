import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'dashboard' },
    strict: true,
    components: {
      default: () => import('./PlaceOfficeApp.vue'),
      drawer: () => import('./PlaceOfficeMenu.vue'),
    },
    children: [
      {
        path: 'dashboard/',
        name: 'dashboard',
        strict: true,
        component: () => import('./pages/DashboardPage.vue'),
      },
    ],
  },
];

export default routes;
