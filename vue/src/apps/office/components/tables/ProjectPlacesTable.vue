<template>
  <data-table
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    :form-component="ProjectPlaceForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import ProjectPlaceForm from '../forms/ProjectPlaceForm.vue';

const { t } = useI18n();

const props = defineProps<{
  projectPlaces: ProjectPlace[];
}>();

const { projectPlaces } = toRefs(props);
const queryColumns = ['name', 'region'];

const columns = [
  {
    name: 'name',
    field: 'name',
    required: true,
    label: t('field.name'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'type',
    field: 'type',
    label: t('field.place_type'),
    align: 'left',
  },
  {
    name: 'mentors',
    field: 'mentors',
    label: t('mentor', 9),
    align: 'left',
  },
  {
    name: 'disciplines',
    field: 'disciplines',
    label: t('discipline', 9),
    align: 'left',
  },
  {
    name: 'region',
    field: 'region',
    label: t('region'),
    align: 'left',
    sortable: true,
  },
];

const rows = computed(() => {
  return projectPlaces.value.map((obj) => ({
    _self: obj,
    name: obj.place.name,
    region: obj.place.region ? obj.place.region.name : '-',
    type: obj.place.type,
    disciplines: obj.disciplines,
  }));
});
</script>
