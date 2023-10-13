<template>
  <q-select
    v-model="model"
    clearable
    dense
    :rounded="asFilter"
    :outlined="asFilter"
    :options="periodOptions"
    :label="label || $t('period')"
    options-dense
    emit-value
    map-options
    :bg-color="asFilter && model !== null ? 'blue-1' : 'white'"
  >
    <template #selected-item="scope">
      <span class="ellipsis">{{ scope.opt.label }}</span>
    </template>
  </q-select>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  periods: Period[];
  asFilter?: boolean;
  label?: string;
}>();

const model = ref<number | null>(null);

const periodOptions = computed(() => {
  if (!props.periods) {
    return [];
  }

  // TODO: check why we are getting empty objects in the array here
  // .filter is a workaround

  return props.periods.filter((obj) => obj).map((period) => ({
    label: period.full_name,
    value: period.id,
  }));
});

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
