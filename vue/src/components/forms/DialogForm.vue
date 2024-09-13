<style lang="scss">
.metis__dialog-layout {
  height: 600px;

  .q-dialog__inner--minimized > & {
    width: 660px !important;
    max-width: 100vw;
  }

  .q-stepper--vertical .q-stepper__tab {
    padding: 12px 24px 12px 20px;
  }

  &.size-sm {
    height: 400px;

    .q-dialog__inner--minimized > & {
      width: 460px !important;
    }
  }
}
</style>

<template>
  <q-layout
    view="hHh lpR fFf"
    container
    class="bg-white metis__dialog-layout metis__form"
    :class="{ 'size-sm': small }"
  >
    <q-header class="bg-white q-pt-sm">
      <q-toolbar class="text-primary q-pl-lg q-pr-sm use-default-q-btn">
        <q-icon :name="icon" />
        <q-toolbar-title v-if="title" class="col-10">
          <span>{{ title }}</span
          ><span v-if="subtitle" class="text-caption q-pl-md">{{ subtitle }}</span>
        </q-toolbar-title>
        <q-space />
        <q-btn flat round v-close-popup icon="close" />
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
  subtitle?: string | undefined;
  small?: boolean;
}>();
</script>
