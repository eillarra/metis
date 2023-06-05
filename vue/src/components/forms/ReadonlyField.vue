<template>
  <q-field :label="label" readonly class="col-12 col-md" dense stack-label>
    <template #control>
      <div class="self-center full-width no-outline" tabindex="0">{{ value }}</div>
    </template>
  </q-field>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  value: string;
}>();
</script>
