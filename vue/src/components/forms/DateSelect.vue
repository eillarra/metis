<template>
  <q-field v-model="model" dense :label="$t('field.date', 9)" :stack-label="model !== null" class="cursor-pointer">
    <template #control>
      <span>{{ dateText }}</span>
    </template>
    <template #append>
      <q-icon ref="calendarBtn" name="event" size="xs" class="q-mx-xs" />
    </template>
    <template #default>
      <q-menu anchor="top end" self="bottom right">
        <q-date v-model="model" mask="YYYY-MM-DD" minimal />
      </q-menu>
    </template>
  </q-field>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { date } from 'quasar';

const emit = defineEmits(['update:modelValue']);

const calendarBtn = ref<HTMLElement | null>(null);
const model = ref<string | null>(null);

const dateText = computed<string>(() => {
  if (!model.value) return '';
  return date.formatDate(model.value, 'YYYY-MM-DD');
});

watch(model, (val) => {
  emit('update:modelValue', val);
});
</script>
