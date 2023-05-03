<template>
  <data-table
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    :form-component="PlaceForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import PlaceForm from '../forms/PlaceForm.vue';

const { t } = useI18n();

const props = defineProps<{
  places: Place[];
}>();

const { places } = toRefs(props);
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
  return places.value.map((place) => ({
    _self: place,
    name: place.institution.name,
    region: place.institution.region ? place.institution.region.name : '-',
    type: place.institution.type,
    mentors: place.contacts
      .filter((contact) => contact.is_mentor)
      .map((contact) => contact.user.name)
      .join(', '),
    disciplines: place.disciplines,
  }));
});
</script>
