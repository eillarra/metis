<template>
  <q-select
    v-model="model"
    :multiple="multiple"
    :rules="rules"
    dense
    :options="props.disciplines"
    :label="$t('discipline', 9)"
    options-dense
    option-value="id"
    option-label="name"
  />
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  disciplines: Discipline[];
  multiple?: boolean;
  rules?: any[];
}>();

const model = ref<number | null>(null);

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
