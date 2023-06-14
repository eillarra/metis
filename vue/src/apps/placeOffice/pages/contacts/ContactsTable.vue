<template>
  <data-table :columns="columns" :rows="rows" sort-by="name" hide-toolbar hide-pagination />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils';

import DataTable from '@/components/tables/DataTable.vue';

const { t } = useI18n();

const props = defineProps<{
  contacts: Contact[];
}>();

const columns = [
  {
    name: 'name',
    field: 'name',
    required: true,
    label: t('field.name'),
    align: 'left',
    sortable: true,
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'is_mentor',
    field: 'is_mentor',
    label: t('mentor'),
    align: 'center',
  },
  {
    name: 'is_admin',
    field: 'is_admin',
    label: t('admin'),
    align: 'center',
  },
  {
    name: 'email',
    field: 'email',
    label: t('field.email'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'last_login',
    field: 'last_login',
    label: t('field.last_login'),
    align: 'left',
    sortable: true,
  },
];

const rows = computed(() => {
  return props.contacts.map((obj) => ({
    name: obj.user.name,
    is_mentor: obj.is_mentor,
    is_staff: obj.is_staff,
    is_admin: obj.is_admin,
    email: obj.user.email,
    last_login: obj.user.last_login ? formatDate(obj.user.last_login) : '-',
  }));
});
</script>
