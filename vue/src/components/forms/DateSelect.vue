<template>
  <q-field
    v-model="mutable"
    dense
    :label="label || $t('field.date', 9)"
    :stack-label="mutable !== null"
    class="cursor-pointer"
    :disable="disable"
    :readonly="readonly"
  >
    <template #control>
      <span>{{ text }}</span>
    </template>
    <template #append v-if="!readonly">
      <q-icon
        ref="calendarBtn"
        :name="calendarType == 'time' ? iconTime : iconCalendarRange"
        size="xs"
        class="q-mx-xs"
      />
    </template>
    <template #default v-if="!readonly">
      <q-menu anchor="top end" self="bottom right">
        <q-time v-if="calendarType == 'time'" v-model="mutable" minimal :format24h="true" :options="options" />
        <q-date v-else v-model="mutable" mask="YYYY-MM-DD" minimal />
      </q-menu>
    </template>
  </q-field>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

import { iconCalendarRange, iconTime } from '@/icons';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  label?: string;
  type?: 'datetime' | 'date' | 'time' | undefined;
  modelValue: string | null;
  options?: (hr: number, min: number | null, sec: number | null) => boolean | null | undefined;
  disable?: boolean;
  readonly?: boolean;
}>();

const calendarBtn = ref<HTMLElement | null>(null);
const calendarType = computed<'datetime' | 'date' | 'time'>(() => {
  if (props.type) return props.type;
  return 'date';
});
const mutable = ref<string | null>(props.modelValue);

const text = computed<string>(() => {
  if (!mutable.value) return '';
  return calendarType.value == 'time' ? mutable.value.substring(0, 5) : mutable.value;
});

watch(mutable, (val) => {
  emit('update:modelValue', val);
});

watch(
  () => props.modelValue,
  (val) => {
    if (val !== mutable.value) mutable.value = val;
  },
);
</script>
