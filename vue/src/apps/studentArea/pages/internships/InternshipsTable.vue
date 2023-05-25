<template>
  <data-table :columns="columns" :rows="rows" sort-by="name" />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';

const { t } = useI18n();

const props = defineProps<{
  internships: Internship[];
}>();

const columns = [
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
    label: t('period'),
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
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    place_name: obj.place?.name || '-',
    block_name: obj.period?.program_internship?.block?.name || '-',
    period_name: obj.period?.program_internship ? `P${obj.period.program_internship.position}` : '-',
    track_name: obj.track?.name || '-',
    disciplines: obj.discipline ? [obj.discipline] : [],
  }));
});
</script>
