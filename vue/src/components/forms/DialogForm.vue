<template>
  <q-layout view="hHh lpR fFf" container class="bg-white" style="width: 600px; max-width: 100vw; max-height: 10px">
    <q-header class="bg-white q-pt-sm">
      <q-toolbar class="text-primary q-px-lg">
        <q-icon :name="icon" />
        <q-toolbar-title v-if="title">{{ title }}</q-toolbar-title>
        <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
      </q-toolbar>
      <q-toolbar class="text-dark text-body1 q-px-lg" style="min-height: auto">
        <slot name="tabs"></slot>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-page class="q-px-sm">
        <slot name="page"></slot>
      </q-page>
    </q-page-container>
    <q-footer class="bg-black text-white">
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
