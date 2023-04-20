const fs = require('fs');
const { resolve } = require('path');

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// read apps folder and create a list of entries
const apps = fs.readdirSync(resolve(__dirname, './vue/src/apps'));
const appsToBuild = {};
apps.forEach((app) => {
  appsToBuild[app] = resolve(__dirname, `./vue/src/apps/${app}/main.ts`);
});


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  root: resolve('./vue/src'),
  base: '/static/vite/',
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.vue', '.js', '.json'],
    alias: {
      '@': resolve(__dirname, './vue/src'),
    },
  },
  build: {
    outDir: resolve('./vue/dist'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: appsToBuild,
      output: {
        chunkFileNames: undefined,
        manualChunks: {
          helpers: ['axios', 'date-fns', 'lodash-es', '@sentry/vue'],
          quasar: ['quasar'],
          vue: ['vue', 'vue-router', 'pinia', 'vue-i18n'],
        },
      },
    },
  },
  define: {
    __VUE_I18N_FULL_INSTALL__: true,
    __VUE_I18N_LEGACY_API__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
  },
});
