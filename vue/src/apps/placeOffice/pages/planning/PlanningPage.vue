<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('planning') }}</h3>
  </div>
  <internships-table :internships="internships" />
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import InternshipsTable from './InternshipsTable.vue';

const { internships } = storeToRefs(useStore());
</script>
