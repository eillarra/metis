<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('internship', 9) }}</h3>
    <div class="col"></div>
  </div>
  <div>
    Deze stages zijn in de "preplanning" fase: je kan een plaats en contactpersoon voorstellen. Stagebureau zal je
    voorstel dan nakijken en goedkeuren. Eens goedgekeurd zal je stage zichtbaar zijn op <a href="..">je dashboard</a>.
  </div>
  <internships-table :internships="internships" class="q-mt-lg" />
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import InternshipsTable from './InternshipsTable.vue';

const store = useStore();

const { internships } = storeToRefs(store);
</script>
