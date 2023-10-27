<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="ContactForm"
    :create-form-component="ContactCreateForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils/dates';

import { useStore } from '../../store.js';

import DataTable from '@/components/tables/DataTable.vue';
import ContactCreateForm from './ContactCreateForm.vue';
import ContactForm from './ContactForm.vue';

const { t } = useI18n();
const store = useStore();
const { education } = storeToRefs(store);

const props = defineProps<{
  contacts: Contact[];
}>();

const queryColumns = ['name', 'email', 'place'];

const allColumns = [
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
    name: 'place',
    field: 'place',
    label: t('place'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'is_mentor',
    field: 'is_mentor',
    label: t('mentor'),
    align: 'center',
  },
  {
    name: 'is_staff',
    field: 'is_staff',
    label: t('staff'),
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

const columnsWithoutStaff = [...allColumns.slice(0, 3), ...allColumns.slice(4, 7)];

const columns = computed(() => {
  if (education.value?.configuration?.place_contact_is_staff === false) {
    return columnsWithoutStaff;
  }
  return allColumns;
});

const rows = computed(() => {
  return props.contacts.map((obj) => ({
    _self: obj,
    name: obj.user.name,
    is_mentor: obj.is_mentor,
    is_staff: obj.is_staff,
    is_admin: obj.is_admin,
    place: obj.Place?.name || '-',
    email: obj.user.email,
    last_login: obj.user.last_login ? formatDate(obj.user.last_login) : '-',
  }));
});
</script>
