import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'planning' },
    strict: true,
    components: {
      default: () => import('./EducationOfficeApp.vue'),
      drawer: () => import('./EducationOfficeMenu.vue'),
    },
    children: [
      {
        path: '/',
        name: 'dashboard',
        strict: true,
        component: () => import('./pages/DashboardPage.vue'),
      },
      {
        path: 'documents/',
        name: 'documents',
        strict: true,
        component: () => import('./pages/documents/DocumentsPage.vue'),
      },
      {
        path: 'planning/',
        name: 'planning',
        strict: true,
        component: () => import('./pages/planning/PlanningPage.vue'),
      },
      {
        path: 'places/',
        name: 'places',
        strict: true,
        component: () => import('./pages/places/PlacesPage.vue'),
      },
      {
        path: 'places/contacts/',
        name: 'placeContacts',
        strict: true,
        component: () => import('./pages/contacts/ContactsPage.vue'),
      },
      {
        path: 'programs/',
        name: 'programs',
        strict: true,
        component: () => import('./pages/ProgramsPage.vue'),
      },
      {
        path: 'project/',
        name: 'project',
        strict: true,
        component: () => import('./pages/ProjectPage.vue'),
      },
      {
        path: 'questionings/',
        name: 'questionings',
        strict: true,
        component: () => import('./pages/questionings/QuestioningsPage.vue'),
      },
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
