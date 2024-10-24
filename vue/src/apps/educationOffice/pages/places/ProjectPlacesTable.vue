<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :hidden-columns="hiddenColumns"
    :form-component="PlaceDialog"
    :create-form-component="ProjectPlaceCreateForm"
    sort-by="name"
    open-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import PlaceDialog from './PlaceDialog.vue';
import ProjectPlaceCreateForm from './ProjectPlaceCreateForm.vue';

const { t } = useI18n();

const props = defineProps<{
  projectPlaces: ProjectPlace[];
}>();

const queryColumns = ['name', 'code'];
const hiddenColumns = ['code'];

const columns = [
  {
    name: 'remarks',
    field: 'remarks',
    required: true,
    label: null,
    align: 'left',
    autoWidth: true,
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
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
    label: t('place_type'),
    align: 'left',
  },
  {
    name: 'has_admins',
    field: 'has_admins',
    label: t('admin', 9),
    align: 'center',
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
];

const rows = computed(() => {
  return props.projectPlaces.map((obj: ProjectPlace) => ({
    _self: obj,
    _class: obj.place.is_flagged ? 'bg-orange-1' : '',
    _remarks_endpoint: obj.place.rel_remarks,
    _remarks_title: obj.place.name,
    _remarks_visibility_options: ['student'],
    remarks: Number(obj.place._tags_dict?.['remarks.count']) || 0,
    name: obj.place.name,
    code: obj.place.code,
    type: obj.place.Type?.name || '-',
    disciplines: obj.Disciplines,
    has_admins: !!obj.place.contacts.filter((contact) => contact.is_admin).length,
    mentors:
      obj.place.contacts
        .filter((contact) => contact.is_mentor)
        .map((contact) => contact.user.name)
        .join(', ') || '-',
  }));
});
</script>
