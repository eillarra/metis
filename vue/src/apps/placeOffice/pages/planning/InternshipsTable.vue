<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="InternshipDialog"
    sort-by="-start_date"
    hide-toolbar
    hide-pagination
    open-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { getEvaluationSteps } from '@/utils/evaluations';

import DataTable from '@/components/tables/DataTable.vue';
import InternshipDialog from './InternshipDialog.vue';

import { useStore } from '../../store.js';

const { t } = useI18n();
const { internships } = storeToRefs(useStore());

const queryColumns = ['student_name', 'place_name'];

const columns = [
  {
    name: 'start_date',
    field: 'start_date',
    required: true,
    label: t('field.start_date'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'end_date',
    field: 'end_date',
    required: true,
    label: t('field.end_date'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'period_name',
    field: 'period_name',
    label: t('period'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'student_name',
    field: 'student_name',
    required: true,
    label: t('student'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'check_hours',
    field: 'check_hours',
    label: t('hour', 9),
    align: 'right',
    autoWidth: true,
    classes: 'panno-mono-number',
    sortable: true,
    sort: (a: [number, boolean], b: [number, boolean]) => a[0] - b[0],
  },
  {
    name: 'steps',
    field: 'evaluation_steps',
    label: t('evaluation', 9),
    align: 'left',
    autoWidth: true,
  },
  {
    name: 'disciplines',
    field: 'disciplines',
    label: t('discipline'),
    align: 'left',
    autoWidth: true,
  },
  {
    name: 'has_mentors',
    field: 'has_mentors',
    label: t('mentor', 9),
    align: 'center',
  },
];

const rows = computed(() => {
  return internships.value.map((obj: Internship) => ({
    _self: obj,
    _class:
      obj.status === 'cancelled'
        ? 'bg-red-1'
        : obj.status === 'unsuccessful'
        ? 'bg-orange-1'
        : !obj.is_approved
        ? 'bg-yellow-1'
        : '',
    start_date: obj.start_date,
    end_date: obj.end_date,
    student_name: (obj.Student?.User as StudentUser)?.name || '-',
    period_name: obj.Period?.full_name || '-',
    check_hours: [
      Number(obj.tag_objects?.['hours.total']?.split(':')[0]) || 0,
      (obj.tag_objects?.['hours.total'] || '-') == (obj.tag_objects?.['hours.approved'] || '-'),
    ],
    evaluation_steps: obj.status === 'definitive' && obj.is_approved ? getEvaluationSteps(obj) : [],
    disciplines: obj.Discipline ? [obj.Discipline] : [],
    has_mentors: obj.mentors.length > 0,
  }));
});
</script>
