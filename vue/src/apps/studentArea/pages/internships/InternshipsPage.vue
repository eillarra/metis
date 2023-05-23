<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('internship', 9) }}</h3>
    <div class="col"></div>
  </div>
  {{ projectStudents }}
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

const { projectStudents } = storeToRefs(useStore());
</script>
