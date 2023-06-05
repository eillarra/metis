<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="InternshipForm"
    :create-form-component="InternshipCreateForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import InternshipCreateForm from './InternshipCreateForm.vue';
import InternshipForm from './InternshipForm.vue';

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
  },
  {
    name: 'block_name',
    field: 'block_name',
    label: t('program_block'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'period_name',
    field: 'period_name',
    label: t('period'),
    align: 'left',
    sortable: true,
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
  },
];

const rows = computed(() => {
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    _class: obj.status === 'cancelled' ? 'bg-red-1' : obj.status === 'unsuccessful' ? 'bg-orange-1' : '',
    student_name: ((obj.student as Student)?.user as User)?.name || '-',
    place_name: obj.place?.name || '-',
    block_name: (((obj.period as Period)?.program_internship as ProgramInternship)?.block as ProgramBlock)?.name || '-',
    period_name: (obj.period as Period)?.program_internship
      ? `P${((obj.period as Period).program_internship as ProgramInternship).position}`
      : '-',
    track_name: (obj.track as Track)?.name || '-',
    disciplines: obj.discipline ? [obj.discipline] : [],
    status: t(`internship_status.${obj.status}`),
  }));
});
</script>
