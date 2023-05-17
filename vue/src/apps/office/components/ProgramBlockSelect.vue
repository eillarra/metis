<template>
  <q-select
    v-model="model"
    clearable
    dense
    :rounded="asFilter"
    :outlined="asFilter"
    :options="blockOptions"
    :label="$t('program_block')"
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
  programs: Program[];
  asFilter?: boolean;
}>();

const model = ref<number | null>(null);

const blockOptions = computed(() => {
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

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
