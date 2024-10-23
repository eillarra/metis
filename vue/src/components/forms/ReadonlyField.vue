<template>
  <q-field :label="label" readonly dense stack-label class="col">
    <template #control>
      <div class="self-center full-width no-outline" tabindex="0">{{ value }}</div>
    </template>
    <template v-if="$slots.prepend" #prepend>
      <slot name="prepend" />
    </template>
    <template v-if="$slots.append" #append>
      <slot name="append" />
    </template>
  </q-field>
</template>

<script setup lang="ts">
defineProps<{
  value: string;
  label?: string;
}>();
</script>
