<style lang="scss">
.ugent__btn {
  font-family: 'UGent Panno Medium', 'Arial', sans-serif;
  font-size: 17px;
  line-height: 15px;
  padding: 12px 15px;

  &.bg-blue {
    background-color: #1e64c8 !important;
  }

  &.bg-yellow {
    background-color: #fdd200 !important;
  }
}
</style>

<template>
  <q-btn
    unelevated
    square
    no-caps
    :icon="icon"
    :label="props.label"
    text-color="dark"
    class="ugent__btn"
    :class="classes"
  />
</template>

<script setup lang="ts">
const props = defineProps<{
  label: string;
  color?: string;
  icon?: string;
}>();

const classes = {
  'bg-blue': props.color === 'blue',
  'bg-yellow': props.color === 'yellow',
};
</script>
