<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :form-component="PlaceProposeForm"
    sort-by="-start_date"
    hide-toolbar
    hide-pagination
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import PlaceProposeForm from './PlaceProposeForm.vue';

const { t } = useI18n();

const props = defineProps<{
  internships: Internship[];
}>();

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
    name: 'place_name',
    field: 'place_name',
    required: true,
    label: t('place'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
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
];

const rows = computed(() => {
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    start_date: obj.start_date,
    end_date: obj.end_date,
    period_name: obj.Period?.full_name || '-',
    place_name: obj.Place?.name || '-',
    student_name: (obj.Student?.User as StudentUser)?.name || '-',
  }));
});
</script>
