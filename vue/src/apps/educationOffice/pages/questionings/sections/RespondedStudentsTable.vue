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

const queryColumns = ['name', 'email'];
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
    name: 'updated_by',
    field: 'updated_by',
    label: t('student'),
    align: 'left',
    sortable: true,
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
      updated_by: obj.updated_by?.name,
      email: obj.updated_by?.email,
      updated_at: formatDate(obj.updated_at),
    };
  });
});
</script>
