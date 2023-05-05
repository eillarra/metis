<template>
  <data-table
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    :form-component="InternshipForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import InternshipForm from '../forms/InternshipForm.vue';

const { t } = useI18n();

const props = defineProps<{
  internships: Internship[];
}>();

const { internships } = toRefs(props);
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
    name: 'block_name',
    field: 'block_name',
    label: t('program_block'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'period_name',
    field: 'period_name',
    label: t('program_internship'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'track_name',
    field: 'track_name',
    label: t('track'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'disciplines',
    field: 'disciplines',
    label: t('discipline'),
    align: 'left',
  },
];

const rows = computed(() => {
  return internships.value.map((obj) => ({
    _self: obj,
    student_name: obj.student?.name || '-',
    place_name: obj.place?.name || '-',
    block_name: obj.program_internship.block?.name,
    period_name: obj.program_internship.name,
    track_name: obj.track?.name || '-',
    disciplines: obj.discipline ? [obj.discipline] : [],
  }));
});
</script>
