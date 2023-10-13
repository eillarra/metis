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
import { useI18n } from 'vue-i18n';

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
    name: 'place_name',
    field: 'place_name',
    required: true,
    label: t('place'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'place_type',
    field: 'place_type',
    label: t('place_type'),
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
];

const rows = computed(() => {
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    _class: obj.status === 'cancelled' ? 'bg-red-1' : obj.status === 'unsuccessful' ? 'bg-orange-1' : '',
    start_date: obj.start_date,
    end_date: obj.end_date,
    place_name: (obj.Place as Place)?.name || '-',
    place_type: (obj.Place as Place)?.Type?.name || '-',
    disciplines: obj.Discipline ? [obj.Discipline] : [],
  }));
});
</script>
