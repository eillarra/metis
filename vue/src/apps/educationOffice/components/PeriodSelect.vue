<template>
  <q-select
    v-model="model"
    clearable
    dense
    :rounded="asFilter"
    :outlined="asFilter"
    :options="periodOptions"
    :label="$t('period')"
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
}>();

const model = ref<number | null>(null);

const periodOptions = computed(() => {
  if (!props.periods) {
    return [];
  }

  return props.periods.map((period) => ({
    label: `${period.program_internship?.block?.name} / P${period.program_internship?.position}`,
    value: period.id,
  }));
});

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
