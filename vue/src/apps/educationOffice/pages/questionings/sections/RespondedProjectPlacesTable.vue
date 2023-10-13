<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    sort-by="-updated_at"
    :rows-per-page="10"
    in-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils';

import DataTable from '@/components/tables/DataTable.vue';

const { t } = useI18n();

const props = defineProps<{
  responses: CustomFormResponse[];
}>();

const queryColumns = ['name', 'updated_by', 'email'];
const columns = [
  {
    name: 'updated_at',
    field: 'updated_at',
    label: t('field.updated_at'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'name',
    field: 'name',
    label: t('place'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'updated_by',
    field: 'updated_by',
    label: t('field.updated_by'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'email',
    field: 'email',
    label: t('field.email'),
    align: 'left',
  },
];

const rows = computed(() => {
  return props.responses.map((obj: CustomFormResponse) => {
    return {
      _self: obj,
      _class: obj._object ? '' : 'bg-red-1',
      name: (obj._object as ProjectPlace)?.place.name ?? `-- ${t('form.deleted')} --`.toLowerCase(),
      updated_by: obj.updated_by?.name,
      email: obj.updated_by?.email,
      updated_at: formatDate(obj.updated_at),
    };
  });
});
</script>
