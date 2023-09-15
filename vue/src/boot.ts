import 'vite/modulepreload-polyfill';

import { createApp, h } from 'vue';
import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { createPinia } from 'pinia';
import { createInertiaApp } from '@inertiajs/vue3';
import { Quasar, Dialog, Notify } from 'quasar';
import * as Sentry from '@sentry/vue';

import langNl from 'quasar/lang/nl';

import { axios, api } from './axios';
import { createI18n, messages } from './i18n';
import { notify } from './notify';
import { storage } from './storage';

const bootApp = (routes: RouteRecordRaw[]) => {
  createInertiaApp({
    resolve: () => {
      return import('./layouts/MainLayout.vue' as string);
    },
    setup({ el, App, props, plugin }) {
      // locale
      storage.set('metis.locale', props.initialPage.props.django_locale);

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
      app.use(Quasar, {
        lang: props.initialPage.props.django_locale === 'nl' ? langNl : undefined,
        plugins: { Dialog, Notify },
      });
      app.use(Router);
      app.use(Store);
      app.use(i18n);

      // axios
      api.interceptors.request.use(
        (config) => {
          if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase() || '')) {
            config.headers['X-CSRFTOKEN'] = props.initialPage.props.django_csrf_token;
          }
          config.headers['Accept-Language'] = props.initialPage.props.django_locale;
          return config;
        },
        (error) => {
          return Promise.reject(error);
        }
      );
      api.interceptors.response.use(
        (res) => res,
        (error) => {
          notify.apiError(error);
          return Promise.reject(error);
        }
      );
      app.config.globalProperties.$axios = axios;
      app.config.globalProperties.$api = api;

      if (!props.initialPage.props.django_debug && props.initialPage.props.sentry_vue_dsn) {
        // sentry
        Sentry.init({
          app,
          dsn: props.initialPage.props.sentry_vue_dsn as string,
          release: props.initialPage.props.git_commit_hash as string,
          environment: props.initialPage.props.django_env as string,
          integrations: [
            new Sentry.BrowserTracing({
              routingInstrumentation: Sentry.vueRouterInstrumentation(Router),
              tracePropagationTargets: ['localhost', 'metis.ugent.be', /^\//],
            }),
          ],
          tracesSampleRate: 0.1,
          // Ignore some errors: https://docs.sentry.io/platforms/javascript/configuration/filtering/
          // - ResizeObserver loop errors
          ignoreErrors: ['ResizeObserver loop'],
        });

        // send user id
        if (props.initialPage.props.django_user) {
          Sentry.setUser({
            id: (props.initialPage.props.django_user as DjangoAuthenticatedUser).id.toString(),
          });
        }
      }

      // mount
      app.mount(el);
    },
  });
};

export { bootApp };
