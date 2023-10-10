<template>
  <data-table :columns="columns" :rows="rows" sort-by="name" hide-toolbar />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils';

import DataTable from '@/components/tables/DataTable.vue';

const { t } = useI18n();

const props = defineProps<{
  signatures: Signature[];
  texts: TextEntry[];
}>();

const columns = [
  {
    name: 'name',
    field: 'name',
    required: true,
    label: t('signature'),
    align: 'left',
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'date',
    field: 'date',
    label: t('field.date'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    classes: 'q-table--col-auto-width',
  },
  {
    name: 'download',
    field: 'download',
    label: 'Download',
    align: 'right',
    classes: 'q-table--col-auto-width',
  },
];

const rows = computed(() => {
  return props.signatures.map((obj: Signature) => ({
    _self: obj,
    name: props.texts.find((text) => text.id === obj.object_id)?.title_nl ?? '',
    date: formatDate(obj.created_at),
    download: obj.url,
  }));
});
</script>
