<template>
  <q-select
    v-model="model"
    :clearable="asFilter"
    dense
    :rounded="asFilter"
    :outlined="asFilter"
    :options="periodOptions"
    :label="label || $t('place_type')"
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
  placeTypes: PlaceType[];
  asFilter?: boolean;
  label?: string;
}>();

const model = ref<number | null>(null);

const periodOptions = computed(() => {
  if (!props.placeTypes) {
    return [];
  }

  return props.placeTypes.map((placeType) => ({
    label: placeType.name,
    value: placeType.id,
  }));
});

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
