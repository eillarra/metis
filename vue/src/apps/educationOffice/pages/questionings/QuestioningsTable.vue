<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :form-component="QuestioningDialog"
    sort-by="-start_at"
    hide-toolbar
    open-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils/dates';

import DataTable from '@/components/tables/DataTable.vue';
import QuestioningDialog from './QuestioningDialog.vue';

const { t, locale } = useI18n();

const props = defineProps<{
  questionings: Questioning[];
}>();

const columns = [
  {
    name: 'period',
    field: 'period',
    label: t('period'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
  },
  {
    name: 'title',
    field: 'title',
    label: t('field.title'),
    align: 'left',
    sortable: true,
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'start_at',
    field: 'start_at',
    label: t('field.start'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'end_at',
    field: 'end_at',
    label: t('field.end'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'is_open',
    field: 'is_open',
    label: t('field.open'),
    align: 'center',
  },
  {
    name: 'has_email',
    field: 'has_email',
    label: t('field.email'),
    align: 'center',
  },
  {
    name: 'progress_responses',
    field: 'progress_responses',
    label: t('response', 9),
    align: 'left',
  },
];

const formTitleByType = {
  project_place_availability: t('questionings.type.project_place_availability'),
  project_place_information: t('questionings.type.project_place_information'),
  student_information: t('questionings.type.student_information'),
  student_tops: t('questionings.type.student_tops'),
};

const rows = computed(() => {
  return props.questionings.map((obj: Questioning) => {
    return {
      _self: obj,
      period: obj.Period?.full_name ?? '-',
      title: obj.form_definition.title
        ? obj.form_definition.title[locale.value as 'nl' | 'en']
        : (formTitleByType[obj.type as keyof typeof formTitleByType] ?? obj.type),
      start_at: formatDate(obj.start_at),
      end_at: formatDate(obj.end_at),
      is_open: obj.is_active,
      has_email: !!obj.email_subject && !!obj.email_body,
      progress_responses: obj.stats?.response_rate ?? 0,
    };
  });
});
</script>
