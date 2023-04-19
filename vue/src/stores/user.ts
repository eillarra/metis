import { defineStore } from 'pinia';
import { pick } from 'lodash-es';

import { api } from '@/axios.ts';

//function mapNotification(obj: UserNotification) {
function mapNotification(obj) {
  return {
    ...obj,
    icon: 'star',
    color: 'grey',
  };
}

export const useUserStore = defineStore('user', {
  state: () => ({
    notifications: [],
    user: null, // null as AuthenticatedUser | null,
  }),

  actions: {
    init() {
      // this.getUser();
    },
    async getNotifications() {
      setTimeout(this.getNotifications, 60 * 1000);

      await api.get('/user/notifications/').then((res) => {
        this.notifications = res.data.map(mapNotification);
      });
    },
    async getUser() {
      await api.get('/user/account/').then((res) => {
        this.user = res.data;
      });
    },
    async updateUser(fields: string[]) {
      await api.patch('/user/account/', pick(this.user, fields)).then((res) => {
        this.user = res.data;
        // notify.success('updated');
      });
    },
  },
});
