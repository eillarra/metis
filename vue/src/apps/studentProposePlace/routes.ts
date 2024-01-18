import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'internships' },
    strict: true,
    components: {
      default: () => import('./StudentProposePlaceApp.vue'),
    },
    children: [
      {
        path: '/',
        name: 'internships',
        strict: true,
        component: () => import('./pages/internships/InternshipsPage.vue'),
      },
    ],
  },
];

export default routes;
