<template>
  <div class="text-center text-grey-5 q-gutter-lg q-my-xl">
    <q-icon :name="icon" size="6em" />
    <div class="text-h5">{{ text }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: string;
  text: string;
}>();
</script>
