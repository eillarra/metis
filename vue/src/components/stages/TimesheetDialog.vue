<template>
  <full-dialog icon="schedule" :title="$t('timesheet')" class="small" hide-drawer>
    <template #page>
      <div class="row q-px-lg q-mb-lg q-col-gutter-y-sm q-col-gutter-x-lg">
        <readonly-field :label="$t('field.date')" :value="obj.date" class="col-12" />
        <readonly-field
          :label="`${$t('field.start_time')} (am)`"
          :value="obj.start_time_am?.substring(0, 5) || '-'"
          class="col-6 col-md-2"
        />
        <readonly-field
          :label="`${$t('field.end_time')} (am)`"
          :value="obj.end_time_am?.substring(0, 5) || '-'"
          class="col-6 col-md-2"
        />
        <readonly-field
          :label="`${$t('field.start_time')} (pm)`"
          :value="obj.start_time_pm?.substring(0, 5) || '-'"
          class="col-6 col-md-2"
        />
        <readonly-field
          :label="`${$t('field.end_time')} (pm)`"
          :value="obj.end_time_pm?.substring(0, 5) || '-'"
          class="col-6 col-md-2"
        />
        <readonly-field
          :label="$t('field.duration')"
          :value="obj.duration?.substring(0, 5) || '-'"
          class="col-6 col-md-4"
        />
      </div>
      <div v-if="obj.data.comments" class="q-mx-lg q-pb-md">
        <strong>{{ $t('form.timesheet.comments') }}</strong>
        <markdown-toast-viewer v-model="dummyBody" :source-text="obj.data.comments" />
      </div>
      <div v-if="obj.data.weekly_reflection" class="q-mx-lg q-pb-md">
        <strong>{{ $t('form.timesheet.weekly_reflection') }}</strong>
        <markdown-toast-viewer v-model="dummyBody" :source-text="obj.data.weekly_reflection" />
      </div>
      <div v-if="obj.data.weekly_action_points" class="q-mx-lg q-pb-md">
        <strong>{{ $t('form.timesheet.weekly_action_points') }}</strong>
        <markdown-toast-viewer v-model="dummyBody" :source-text="obj.data.weekly_action_points" />
      </div>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import FullDialog from '@/components/FullDialog.vue';
import MarkdownToastViewer from '@/components/forms/MarkdownToastViewer.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';

defineProps<{
  obj: Timesheet;
}>();

const dummyBody = ref<string>('');
</script>
