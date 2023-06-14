import { RouteRecordRaw } from 'vue-router';

import { useStore } from './store';

function isPlaceAdmin() {
  if (!useStore().userIsAdmin) return { name: 'dashboard' };
}

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
      // --- for is_admin
      {
        path: 'address/',
        name: 'address',
        strict: true,
        component: () => import('./pages/AddressPage.vue'),
        beforeEnter: [isPlaceAdmin],
      },
      {
        path: 'contacts/',
        name: 'contacts',
        strict: true,
        component: () => import('./pages/contacts/ContactsPage.vue'),
        beforeEnter: [isPlaceAdmin],
      },
    ],
  },
];

export default routes;
