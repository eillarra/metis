import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'planning' },
    strict: true,
    components: {
      default: () => import('./OfficeApp.vue'),
      drawer: () => import('./OfficeMenu.vue'),
    },
    children: [
      {
        path: '/',
        name: 'dashboard',
        strict: true,
        component: () => import('./pages/DashboardPage.vue'),
      },
      {
        path: 'planning/',
        name: 'planning',
        strict: true,
        component: () => import('./pages/PlanningPage.vue'),
      },
      {
        path: 'places/',
        name: 'places',
        strict: true,
        component: () => import('./pages/PlacesPage.vue'),
      },
      {
        path: 'places/contacts/',
        name: 'placeContacts',
        strict: true,
        component: () => import('./pages/ContactsPage.vue'),
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
