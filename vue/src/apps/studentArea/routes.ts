import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'tasks' },
    strict: true,
    components: {
      default: () => import('./StudentAreaApp.vue'),
      drawer: () => import('./StudentAreaMenu.vue'),
    },
    children: [
      {
        path: 'internships/',
        name: 'internships',
        strict: true,
        component: () => import('./pages/internships/InternshipsPage.vue'),
      },
      {
        path: 'signatures/',
        name: 'signatures',
        strict: true,
        component: () => import('./pages/signatures/SignaturesPage.vue'),
      },
      {
        path: 'tasks/',
        name: 'tasks',
        strict: true,
        component: () => import('./pages/tasks/TasksPage.vue'),
      },
    ],
  },
];

export default routes;
