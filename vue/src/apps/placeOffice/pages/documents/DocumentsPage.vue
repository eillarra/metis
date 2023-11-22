<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('document', 9) }}</h3>
    <div class="col"></div>
  </div>
  <ul>
    <li v-for="file in files" :key="file.id">
      <a :href="file.url" target="_blank">{{ file.description }}</a>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

const page = usePage();

const files = computed<RelatedFile[]>(() =>
  ((page.props.files as RelatedFile[]) ?? []).filter((file) => file.code.startsWith('place:'))
);
</script>
