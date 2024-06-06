<template>
  <q-field :label="label" readonly dense stack-label class="col">
    <template #control>
      <div class="self-center full-width no-outline" tabindex="0">{{ value }}</div>
    </template>
    <template #append>
      <slot name="append" />
    </template>
  </q-field>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  value: string;
}>();
</script>
