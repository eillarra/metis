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
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import ContactCreateForm from './ContactCreateForm.vue';
import ContactForm from './ContactForm.vue';

const { t } = useI18n();

const props = defineProps<{
  contacts: Contact[];
}>();

const queryColumns = ['name', 'email', 'place'];

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
    name: 'email',
    field: 'email',
    label: t('field.email'),
    align: 'left',
    sortable: true,
  },
];

const rows = computed(() => {
  return props.contacts.map((obj) => ({
    _self: obj,
    name: obj.user.name,
    is_mentor: obj.is_mentor,
    is_staff: obj.is_staff,
    place: obj.Place?.name || '-',
    email: obj.user.email,
  }));
});
</script>
