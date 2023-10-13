<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    sort-by="name"
    :rows-per-page="10"
    in-dialog
    :selection="questioningIsOpen ? 'multiple' : 'none'"
    v-model:selected="selected"
  >
    <template #selected-action v-if="questioningIsOpen">
      <div class="col-6 col-md-2 ugent__create-btn">
        <q-btn
          unelevated
          color="blue-1"
          :label="`&nbsp;${$t('form.send_email')}`"
          icon="send"
          class="text-ugent full-width"
          :disable="selected.length === 0"
          @click="sendEmails"
        />
      </div>
    </template>
  </data-table>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { useCommonStore } from '@/stores/common.js';
import { confirm } from '@/dialog';
import { notify } from '@/notify';
import { formatDate } from '@/utils';

import DataTable from '@/components/tables/DataTable.vue';

const { t } = useI18n();

const { now } = storeToRefs(useCommonStore());

const props = defineProps<{
  questioning: Questioning;
  projectPlaces: ProjectPlace[];
}>();

const selected = ref([]);
const queryColumns = ['name', 'admin', 'email'];
const columns = [
  {
    name: 'name',
    field: 'name',
    label: t('place'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'contact',
    field: 'contact',
    label: t('admin'),
    align: 'left',
    sortable: true,
    autoWidth: true,
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
  return props.projectPlaces.map((obj: ProjectPlace) => {
    const adminContact: Contact = obj.place.contacts.find((contact) => contact.is_admin) as Contact;
    return {
      _self: obj,
      name: obj.place.name,
      contact: adminContact?.user.name || '-',
      email: adminContact?.user.email || '-',
      last_login: adminContact?.user.last_login ? formatDate(adminContact?.user.last_login) : '-',
    };
  });
});

const questioningIsOpen = computed(() => {
  return new Date(props.questioning.end_at) > now.value && now.value > new Date(props.questioning.start_at);
});

const selectedIds = computed(() => {
  return selected.value.map((obj) => (obj._self as ProjectPlace).id);
});

function sendEmails() {
  if (!questioningIsOpen.value || !selectedIds.value.length) return;

  confirm(t('form.questioning.confirm_send_emails', { count: selectedIds.value.length }), () => {
    api.post(`${props.questioning.self}send_emails/`, { ids: selectedIds.value }).then(() => {
      notify.success(t('form.questioning.emails_sent', selectedIds.value.length));
      selected.value = [];
    });
  });
}
</script>
