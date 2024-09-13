<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">{{ $t('contact', 9) }}</h4>
  </div>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="ContactForm"
    :create-form-component="ContactCreateForm"
    :create-parent="obj.place"
    sort-by="name"
    hide-column-selector
    removable
    @remove:row="removeContact"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { confirm } from '@/dialog';
import { notify } from '@/notify';
import { formatDate } from '@/utils/dates';

import { useStore } from '../../store.js';

import DataTable from '@/components/tables/DataTable.vue';
import ContactCreateForm from '../contacts/ContactCreateForm.vue';
import ContactForm from '../contacts/ContactForm.vue';

const props = defineProps<{
  obj: ProjectPlace;
}>();

const { t } = useI18n();
const store = useStore();
const { education, places } = storeToRefs(store);

const processing = ref(false);
const queryColumns = ['name', 'email', 'place'];
// compute to get an updated list of contacts when contacts are added or removed
const place = computed<Place | undefined>(() => places.value.find((p) => p.id === props.obj.place.id));

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
  return (place.value?.contacts || []).map((obj) => ({
    _self: obj,
    name: obj.user.name,
    is_mentor: obj.is_mentor,
    is_staff: obj.is_staff,
    is_admin: obj.is_admin,
    email: obj.user.email,
    last_login: obj.user.last_login ? formatDate(obj.user.last_login) : '-',
  }));
});

function removeContact(row: { _self: Contact }) {
  if (processing.value) return;

  confirm(t('form.contact.confirm_delete', { name: row._self.user.name }), () => {
    processing.value = true;

    api
      .delete(row._self.self)
      .then(() => {
        store.deleteObj('contact', row._self);
        notify.success(t('form.contact.deleted'));
      })
      .finally(() => {
        processing.value = false;
      });
  });
}
</script>
