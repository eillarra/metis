import 'vite/modulepreload-polyfill';

import { createApp, h } from 'vue';
import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { createPinia } from 'pinia';
import { createInertiaApp } from '@inertiajs/vue3';
import { Quasar } from 'quasar';
import * as Sentry from '@sentry/vue';

import { axios, api } from './axios.ts';
import { createI18n, messages } from './i18n.ts';

const bootApp = (routes: RouteRecordRaw[]) => {
  createInertiaApp({
    resolve: () => {
      return import('./layouts/MainLayout.vue');
    },
    setup({ el, App, props, plugin }) {
      // i18n
      const i18n = createI18n({
        legacy: false,
        locale: props.initialPage.props.django_locale,
        fallbackLocale: {
          default: ['en'],
        },
        messages,
      });

      // router
      const Router = createRouter({
        history: createWebHashHistory(),
        routes,
      });

      // pinia
      const Store = createPinia();

      // app
      const app = createApp({ render: () => h(App, props) });
      app.use(plugin);
      app.use(Quasar, {});
      app.use(Router);
      app.use(Store);
      app.use(i18n);

      // axios
      app.config.globalProperties.$axios = axios;
      app.config.globalProperties.$api = api;

      if (!props.initialPage.props.django_debug) {
        // sentry
        Sentry.init({
          app,
          dsn: 'https://0c8a62299e0b46c9b472cdf6e69e8484@o124046.ingest.sentry.io/4505041367924736',
          release: props.initialPage.props.git_commit_hash,
          environment: 'production',
          integrations: [
            new Sentry.BrowserTracing({
              routingInstrumentation: Sentry.vueRouterInstrumentation(Router),
              tracePropagationTargets: ['localhost', 'tw06v070.ugent.be', /^\//],
            }),
          ],
          tracesSampleRate: 0.1,
          // Ignore some errors: https://docs.sentry.io/platforms/javascript/configuration/filtering/
          // - ResizeObserver loop errors
          ignoreErrors: ['ResizeObserver loop'],
        });
      }

      // mount
      app.mount(el);
    },
  });
};

export { bootApp };
