<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :hidden-columns="hiddenColumns"
    :form-component="ProjectPlaceForm"
    :create-form-component="ProjectPlaceCreateForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import ProjectPlaceCreateForm from './ProjectPlaceCreateForm.vue';
import ProjectPlaceForm from './ProjectPlaceForm.vue';

const { t } = useI18n();

const props = defineProps<{
  projectPlaces: ProjectPlace[];
}>();

const queryColumns = ['name', 'code'];
const hiddenColumns = ['code'];

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
    name: 'code',
    field: 'code',
    label: t('field.code'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
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
  return props.projectPlaces.map((obj: ProjectPlace) => ({
    _self: obj,
    name: obj.place.name,
    code: obj.place.code,
    region: obj.place.region ? obj.place.region.name : '-',
    type: obj.place.type,
    disciplines: obj.disciplines,
    mentors:
      obj.place.contacts
        .filter((contact) => contact.is_mentor)
        .map((contact) => contact.user.name)
        .join(', ') || '-',
  }));
});
</script>
