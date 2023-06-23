import { RouteRecordRaw } from 'vue-router';

import { useStore } from './store';

function isPlaceAdmin() {
  if (!useStore().userIsAdmin) return { name: 'tasks' };
}

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: { name: 'tasks' },
    strict: true,
    components: {
      default: () => import('./PlaceOfficeApp.vue'),
      drawer: () => import('./PlaceOfficeMenu.vue'),
    },
    children: [
      {
        path: 'tasks/',
        name: 'tasks',
        strict: true,
        component: () => import('./pages/tasks/TasksPage.vue'),
      },
      // --- for is_admin
      {
        path: 'addresses/',
        name: 'addresses',
        strict: true,
        component: () => import('./pages/AddressesPage.vue'),
        beforeEnter: [isPlaceAdmin],
      },
      {
        path: 'contacts/',
        name: 'contacts',
        strict: true,
        component: () => import('./pages/contacts/ContactsPage.vue'),
      },
    ],
  },
];

export default routes;
