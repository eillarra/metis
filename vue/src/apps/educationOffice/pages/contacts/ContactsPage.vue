<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none use-default-q-btn">
      {{ $t('contact', 9) }}
      <q-btn
        v-if="contacts.length"
        round
        outline
        :href="contactsExcelPath"
        target="_blank"
        :icon="iconDownload"
        size="sm"
        color="primary"
        class="q-ml-md q-pa-xs"
      >
        <q-tooltip :delay="250">{{ $t('download.excel') }}</q-tooltip>
      </q-btn>
    </h3>
    <div class="col"></div>
    <q-select
      v-model="selectedProfile"
      clearable
      dense
      rounded
      outlined
      :options="profileOptions"
      :label="$t('profile')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedProfile !== null ? 'blue-1' : 'white'"
    >
      <template #selected-item="scope">
        <span class="ellipsis">{{ scope.opt.label }}</span>
      </template>
    </q-select>
  </div>
  <contacts-table v-if="project" :contacts="filteredContacts" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { useStore } from '../../store.js';

import ContactsTable from './ContactsTable.vue';

import { iconDownload } from '@/icons';

const { t } = useI18n();
const { project, contacts } = storeToRefs(useStore());

const selectedProfile = ref<string | null>(null);

const contactsExcelPath = computed(() => {
  return `/nl/files/p/proj_${project.value?.id}_contacts.xlsx`;
});

const profileOptions = [
  {
    label: t('staff'),
    value: 'staff',
  },
  {
    label: t('mentor'),
    value: 'mentor',
  },
  {
    label: t('contact_only'),
    value: 'contact_only',
  },
];

const filteredContacts = computed<Contact[]>(() => {
  return contacts.value.filter((obj) =>
    selectedProfile.value
      ? (selectedProfile.value == 'staff' && obj.is_staff) ||
        (selectedProfile.value == 'mentor' && obj.is_mentor) ||
        (selectedProfile.value == 'contact_only' && !obj.is_staff && !obj.is_mentor)
      : true,
  );
});
</script>
