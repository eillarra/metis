<template>
  <data-table
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    :form-component="ContactForm"
    sort-by="name"
  >
  </data-table>
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import ContactForm from '../forms/ContactForm.vue';

const { t } = useI18n();

const props = defineProps<{
  contacts: Contact[];
}>();

const { contacts } = toRefs(props);
const queryColumns = ['name', 'email'];

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
    name: 'places',
    field: 'places',
    label: t('place', 9),
    align: 'left',
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
  return contacts.value.map((contact) => ({
    _self: contact,
    name: contact.user.name,
    is_mentor: contact.is_mentor,
    is_staff: contact.is_staff,
    places: contact.institutions?.map((institution) => institution.name).join(', ') || '-',
    email: contact.user.email,
  }));
});
</script>
