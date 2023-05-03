<template>
  <q-select
    dense
    square
    outlined
    v-model="model"
    :options="blockFilters"
    :label="$t('program_block')"
    clearable
    options-dense
    emit-value
    map-options
  >
    <template #prepend>
      <q-icon name="filter_alt" />
    </template>
  </q-select>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const props = defineProps<{
  programs: Program[];
}>();

const model = ref<number | null>(null);

const blockFilters = computed(() => {
  if (!props.programs) {
    return [];
  }

  return props.programs.reduce((acc: object[], program: Program) => {
    return [
      ...acc,
      ...program.blocks.map((block: ProgramBlockTiny) => {
        return {
          value: block.id,
          label: block.name,
        };
      }),
    ];
  }, []);
});
</script>
