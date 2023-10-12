<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="InternshipDialog"
    :create-form-component="InternshipCreateForm"
    sort-by="name"
    open-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import InternshipCreateForm from './InternshipCreateForm.vue';
import InternshipDialog from './InternshipDialog.vue';

const { t } = useI18n();

const props = defineProps<{
  internships: Internship[];
}>();

const queryColumns = ['student_name', 'place_name'];

const columns = [
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
    name: 'place_name',
    field: 'place_name',
    required: true,
    label: t('place'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
  },
  {
    name: 'track_name',
    field: 'track_name',
    label: t('track'),
    align: 'left',
    sortable: true,
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'block_name',
    field: 'block_name',
    label: t('program_block'),
    align: 'left',
    sortable: true,
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'period_name',
    field: 'period_name',
    label: t('period'),
    align: 'left',
    sortable: true,
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'disciplines',
    field: 'disciplines',
    label: t('discipline'),
    align: 'left',
  },
  {
    name: 'status',
    field: 'status',
    label: t('field.status'),
    align: 'left',
    sortable: true,
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'start_date',
    field: 'start_date',
    label: t('field.start_date'),
    align: 'left',
    sortable: true,
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'end_date',
    field: 'end_date',
    label: t('field.end_date'),
    align: 'left',
    sortable: true,
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'has_mentors',
    field: 'has_mentors',
    label: t('mentor', 9),
    align: 'center',
  },
];

const rows = computed(() => {
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    _class: obj.status === 'cancelled' ? 'bg-red-1' : obj.status === 'unsuccessful' ? 'bg-orange-1' : '',
    student_name: (obj.Student?.User as StudentUser)?.name || '-',
    place_name: obj.Place?.name || '-',
    block_name: obj.Period?.ProgramInternship?.Block?.name || '-',
    period_name: obj.Period?.ProgramInternship ? `P${obj.Period.ProgramInternship.position}` : '-',
    track_name: obj.Track?.name || '-',
    disciplines: obj.Discipline ? [obj.Discipline] : [],
    status: t(`internship_status.${obj.status}`),
    start_date: obj.start_date,
    end_date: obj.end_date,
    has_mentors: obj.mentors.length > 0,
  }));
});
</script>
