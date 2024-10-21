<template>
  <full-dialog :icon="iconTimesheet" :title="$t('timesheet')" class="small" hide-drawer>
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
      <div v-if="formDefinition && obj.data" class="q-mt-xl q-mx-lg q-pb-md">
        <custom-form-viewer :form-definition="formDefinition" :data="obj.data" />
      </div>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

import FullDialog from '@/components/FullDialog.vue';
import CustomFormViewer from '@/components/custom_forms/CustomFormViewer.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';

import { iconTimesheet } from '@/icons';

defineProps<{
  obj: Timesheet;
}>();

// --
const page = usePage();
const formDefinition = computed<CustomFormDefinition | null>(
  () => (page.props.education as Education).configuration?.timesheets_extra_form || null,
);
// --
</script>
