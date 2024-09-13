<template>
  <q-card bordered class="use-default-q-btn">
    <q-card-section class="full-width">
      <div class="text-body1 ellipsis-3-lines">{{ title }}</div>
    </q-card-section>
    <q-space />
    <q-card-section class="q-pt-none">
      <q-skeleton type="text" animation="none" />
      <q-skeleton type="text" animation="none" width="60%" />
    </q-card-section>
    <q-separator />
    <q-card-actions class="use-default-q-btn">
      <slot name="actions" />
    </q-card-actions>
  </q-card>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
}>();
</script>
