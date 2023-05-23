<style lang="scss">
.metis__dialog-layout {
  .q-dialog__inner--minimized > & {
    width: 600px !important;
    max-width: 100vw;
  }

  .q-stepper--vertical .q-stepper__tab {
    padding: 12px 24px 12px 20px;
  }
}
</style>

<template>
  <q-layout view="hHh lpR fFf" container class="bg-white metis__dialog-layout metis__form" style="height: 600px">
    <q-header class="bg-white q-pt-sm">
      <q-toolbar class="text-primary q-pl-lg q-pr-sm">
        <q-icon :name="icon" />
        <q-toolbar-title v-if="title">{{ title }}</q-toolbar-title>
        <q-space />
        <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
      </q-toolbar>
      <q-toolbar class="text-dark text-body1 q-px-lg" style="min-height: auto">
        <slot name="tabs"></slot>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-page>
        <slot name="page"></slot>
      </q-page>
    </q-page-container>
    <q-footer class="bg-white">
      <slot name="footer"></slot>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
defineProps<{
  icon: string;
  title: string | undefined;
}>();
</script>
