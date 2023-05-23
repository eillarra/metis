import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'students' },
    strict: true,
    components: {
      default: () => import('./PlaceOfficeApp.vue'),
      drawer: () => import('./PlaceOfficeMenu.vue'),
    },
    children: [
      {
        path: 'students/',
        name: 'students',
        strict: true,
        component: () => import('./pages/students/StudentsPage.vue'),
      },
    ],
  },
];

export default routes;
