<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ $t('evaluation', 9) }}
    </h4>
  </div>
  <ul>
    <li v-for="evaluation in evaluations" :key="evaluation.id">
      <a :href="evaluation.url" target="_blank">{{ evaluation.url }}</a>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

import { api } from '@/axios.ts';

const props = defineProps<{
  internship: Internship;
}>();

const evaluations = ref<Evaluation[]>([]);

function fetchEvaluations() {
  api.get(props.internship.rel_evaluations).then((response) => {
    evaluations.value = response.data as Evaluation[];
  });
}

onMounted(() => {
  fetchEvaluations();
});
</script>
