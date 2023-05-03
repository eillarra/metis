<template>
  <div class="row q-col-gutter-sm q-mb-sm">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('place_contact', 9) }}</h3>
  </div>
  <contacts-table v-if="project" :contacts="contacts" />
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useOfficeStore } from '../store';

import ContactsTable from '../components/tables/ContactsTable.vue';

const { project, contacts } = storeToRefs(useOfficeStore());
</script>
