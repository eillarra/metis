<template>
  <q-field
    v-model="model"
    clearable
    dense
    rounded
    outlined
    :label="$t('field.date', 9)"
    :stack-label="model !== null"
    class="cursor-pointer"
    :bg-color="model !== null ? 'blue-1' : 'white'"
  >
    <template #control>
      <span>{{ datesText }}</span>
    </template>
    <template #append>
      <q-icon ref="calendarBtn" name="event" size="xs" class="q-mx-xs" />
    </template>
    <template #default>
      <q-menu anchor="top end" self="bottom right">
        <q-date v-model="model" range minimal />
      </q-menu>
    </template>
  </q-field>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

import { formatDate } from '@/utils/dates';

const emit = defineEmits(['update:modelValue']);

const calendarBtn = ref<HTMLElement | null>(null);
const model = ref<QuasarDateRange | null>(null);

const datesText = computed<string>(() => {
  if (!model.value) return '';
  const { from, to } = model.value;
  const fromDate = formatDate(from, 'D/M');
  const toDate = formatDate(to, 'D/M');
  return `${fromDate} - ${toDate}`;
});

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
