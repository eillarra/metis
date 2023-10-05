<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="InternshipDialog"
    sort-by="name"
    hide-toolbar
    hide-pagination
    open-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils';

import DataTable from '@/components/tables/DataTable.vue';
import InternshipDialog from './InternshipDialog.vue';

const { t } = useI18n();

const props = defineProps<{
  internships: Internship[];
}>();

const queryColumns = ['student_name', 'place_name'];

const columns = [
  {
    name: 'start_date',
    field: 'start_date',
    required: true,
    label: t('field.start_date'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'end_date',
    field: 'end_date',
    required: true,
    label: t('field.end_date'),
    align: 'left',
    sortable: true,
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
    name: 'disciplines',
    field: 'disciplines',
    label: t('discipline'),
    align: 'left',
  },
];

const rows = computed(() => {
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    _class: obj.status === 'cancelled' ? 'bg-red-1' : obj.status === 'unsuccessful' ? 'bg-orange-1' : '',
    start_date: obj.start_date ? formatDate(obj.start_date, 'YYYY-MM-DD (dddd)').toLowerCase() : '-',
    end_date: obj.end_date ? formatDate(obj.end_date, 'YYYY-MM-DD (dddd)').toLowerCase() : '-',
    student_name: (obj.Student?.User as StudentUser)?.name || '-',
    disciplines: obj.Discipline ? [obj.Discipline] : [],
  }));
});
</script>
