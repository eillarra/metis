<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('questioning', 9) }}</h3>
  </div>
  <questionings-table v-if="questionings" :questionings="questionings" />
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import QuestioningsTable from './QuestioningsTable.vue';

const store = useStore();

const { questionings } = storeToRefs(store);

store.fetchQuestionings();
</script>
