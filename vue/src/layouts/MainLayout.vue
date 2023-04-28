<template>
  <div class="container">
    <q-layout view="hhh lpR fff">
      <q-header class="row ugent__header bg-white">
        <q-toolbar class="col-3 col-md-2 bg-white q-pl-none q-pt-md">
          <a href="/" class="q-mr-sm">
            <img v-if="django_locale == 'nl'" src="@/assets/ugent.svg" class="logo q-mr-sm" />
            <img v-else src="@/assets/ugent_en.svg" class="logo q-mr-sm" />
          </a>
        </q-toolbar>
        <q-toolbar
          class="col-9 col-md-10 bg-ugent text-white q-pl-md q-pb-sm"
          :class="{ 'q-pl-lg': $q.screen.gt.sm }"
          style="align-items: flex-end"
        >
          <h2 class="text-uppercase q-ma-none">Metis</h2>
          <div
            class="absolute-top-right header-links text-white q-py-sm q-px-md q-gutter-x-lg"
            :class="{ 'q-py-md q-px-lg': $q.screen.gt.sm }"
          >
            <a v-if="django_user && django_user.is_staff" href="/admin/">Admin</a>
            <user-menu v-if="django_user" :user="django_user" />
            <a v-else href="/u/login/"
              ><span v-t="'user_menu.login'"></span> <q-icon name="login" size="xxs"></q-icon
            ></a>
            <locale-menu :locale="django_locale" :csrfToken="django_csrf_token" />
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer
        show-if-above
        v-model="leftDrawer"
        side="left"
        :elevated="$q.screen.lt.md"
        class="q-pt-lg text-weight-medium"
        :width="210"
      >
        <router-view name="drawer" />
      </q-drawer>

      <q-page-container>
        <router-view />
      </q-page-container>

      <q-footer
        class="ugent__footer bg-ugent text-white q-py-lg q-mt-xl full-width q-px-md"
        :class="{ 'q-px-lg': $q.screen.gt.sm }"
      >
        <div class="row justify-between text-body2">
          <div class="col-12 col-md">
            <p>
              <span v-t="'version'"></span>&nbsp;<a
                v-if="django_user && django_user.is_staff"
                :href="`https://github.ugent.be/eillarra/metis/tree/${git_commit_hash}`"
                >{{ version }}</a
              ><span v-else>{{ version }}</span>
            </p>
          </div>
          <div class="col-12 col-md-9">
            <ul :class="{ 'text-right q-gutter-x-md': $q.screen.gt.sm }">
              <li :class="{ inline: $q.screen.gt.sm }">
                <a :href="`mailto:${helpdeskEmail}`">Feedback</a>
              </li>
              <li :class="{ inline: $q.screen.gt.sm }">
                <span
                  >&copy; {{ year }}
                  <a v-t="'ge'" :href="`https://www.ugent.be/ge/${django_locale}`" target="_blank" rel="noopener"></a>,
                  <span v-t="'ugent'" class="text-no-wrap"></span
                ></span>
              </li>
            </ul>
          </div>
        </div>
      </q-footer>
    </q-layout>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import LocaleMenu from '@/components/LocaleMenu.vue';
import UserMenu from '@/components/UserMenu.vue';

// get basic info from Django
const props = defineProps<{
  django_csrf_token: string;
  django_debug: boolean;
  django_locale: string;
  django_user: DjangoAuthenticatedUser | null;
  git_commit_hash: string;
}>();

const version = props.git_commit_hash.substring(0, 7);
const helpdeskEmail = 'helpdesk.metis@ugent.be';
const year = new Date().getFullYear();

const leftDrawer = ref(false);
</script>
