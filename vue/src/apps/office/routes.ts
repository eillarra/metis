import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    name: 'home',
    strict: true,
    components: {
      default: () => import('./OfficeApp.vue'),
      drawer: () => import('./OfficeMenu.vue'),
    },
    children: [
      {
        path: 'calendar/',
        name: 'calendar',
        strict: true,
        component: () => import('./pages/CalendarPage.vue'),
      },
      {
        path: 'places/',
        name: 'places',
        strict: true,
        component: () => import('./pages/PlacesPage.vue'),
      },
      {
        path: 'programs/',
        name: 'programs',
        strict: true,
        component: () => import('./pages/ProgramsPage.vue'),
      },
      {
        path: 'students/',
        name: 'students',
        strict: true,
        component: () => import('./pages/StudentsPage.vue'),
      },
    ],
  },
];

export default routes;