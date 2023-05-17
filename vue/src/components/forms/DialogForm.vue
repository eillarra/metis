<style lang="scss">
.metis__dialog-layout {
  width: 600px !important;
  max-width: 100vw;

  .q-field--dense .q-field__control {
    height: 44px;
  }

  .q-stepper--vertical .q-stepper__tab {
    padding: 12px 24px 12px 20px;
  }
}
</style>

<template>
  <q-layout view="hHh lpR fFf" container class="bg-white metis__dialog-layout" style="height: 600px">
    <q-header class="bg-white q-pt-sm">
      <q-toolbar class="text-primary q-pl-lg q-pr-sm">
        <q-icon :name="icon" />
        <q-toolbar-title v-if="title">{{ title }}</q-toolbar-title>
        <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
      </q-toolbar>
      <q-toolbar class="text-dark text-body1 q-px-lg" style="min-height: auto">
        <slot name="tabs"></slot>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-page>
        <slot name="page"></slot>
        <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
          <q-btn fab icon="keyboard_arrow_up" color="accent" />
        </q-page-scroller>
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
