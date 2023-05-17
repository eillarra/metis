<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('contact', 9) }}</h3>
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

import { useOfficeStore } from '../store';

import ContactsTable from '../components/tables/ContactsTable.vue';

const { t } = useI18n();
const { project, contacts } = storeToRefs(useOfficeStore());

const selectedProfile = ref<string | null>(null);

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
      : true
  );
});
</script>
