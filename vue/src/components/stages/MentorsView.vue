<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ $t('mentor', 9) }}
    </h4>
  </div>
  <data-table
    :columns="columns"
    :rows="rows"
    sort-by="name"
    hide-toolbar
    hide-pagination
    :removable="editable"
    @remove:row="removeMentor"
  />
  <div v-if="editable">
    <h6 class="col-12 col-md-3 q-my-md">{{ $t('contact', 9) }}</h6>
    <div class="row q-col-gutter-lg" v-if="availableContacts.length">
      <div class="col-12 col-md-4" v-for="contact in availableContacts" :key="contact.id">
        <q-card square bordered flat>
          <q-card-section class="q-pt-xs">
            <div class="q-my-md">{{ contact.user.name }}</div>
            <div class="text-body2">
              <div v-if="contact.is_admin">- {{ $t('admin') }}</div>
              <div v-if="contact.is_mentor">- {{ $t('mentor') }}</div>
              <div>- {{ $t('field.last_login') }}: {{ contact.lastLogin }}</div>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-actions>
            <q-btn dense :disable="processing" flat color="ugent" @click="addMentor(contact.user.id)">
              {{ $t('form.add') }}
            </q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
    <div v-else class="row q-col-gutter-lg q-mr-lg">
      <div class="col-12 col-md-4">
        <div class="bg-yellow-2 q-pa-md">{{ $t('form.mentor.no_more_contacts') }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { confirm } from '@/dialog';
import { notify } from '@/notify';
import { formatDate } from '@/utils/dates';

import DataTable from '@/components/tables/DataTable.vue';

const emit = defineEmits(['update:obj']);

const props = defineProps<{
  obj: Internship;
  editable?: boolean;
}>();

const { t } = useI18n();

const obj = ref<Internship>(props.obj);
const processing = ref<boolean>(false);

const availableContacts = computed<Contact[]>(() => {
  if (!obj.value.Place) return [];
  return obj.value.Place.contacts
    .filter((c) => c.is_mentor && !obj.value.mentors.find((m) => m.user.id === c.user.id))
    .map((obj: Contact) => ({
      ...obj,
      lastLogin: obj.user.last_login ? formatDate(obj.user.last_login) : '-',
    }));
});

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
    name: 'email',
    field: 'email',
    label: t('field.email'),
    align: 'left',
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
  return props.obj.mentors.map((obj: Mentor) => ({
    _self: obj,
    name: obj.user.name,
    email: obj.user.email,
    last_login: obj.user.last_login ? formatDate(obj.user.last_login) : '-',
  }));
});

function addMentor(userId: number) {
  processing.value = true;
  api
    .post(`${obj.value.self}add_mentor/`, { user_id: userId })
    .then((res) => {
      obj.value.mentors.push(res.data);
      notify.success(t('form.mentor.added'));
      emit('update:obj', obj.value);
    })
    .finally(() => {
      processing.value = false;
    });
}

function removeMentor(row: { _self: object }) {
  confirm(t('form.mentor.confirm_delete'), () => {
    const userId = (row._self as Mentor).user.id;
    processing.value = true;
    api
      .post(`${obj.value.self}remove_mentor/`, { user_id: userId })
      .then(() => {
        obj.value.mentors = obj.value.mentors.filter((m) => m.user.id !== userId);
        notify.success(t('form.mentor.deleted'));
        emit('update:obj', obj.value);
      })
      .finally(() => {
        processing.value = false;
      });
  });
}
</script>
