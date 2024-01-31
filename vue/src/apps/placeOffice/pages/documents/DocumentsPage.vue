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
  <div v-if="education.code == 'geneeskunde'">
    <strong>Studentenfiches</strong>
    <ul>
      <li v-for="internship in internships" :key="internship.id">
        <a :href="`/files/i/${ internship.uuid }_affiche.pdf`" target="_blank">{{ internship.Student?.User?.name }}: affiche voor de wachtzaal</a>
        <!--<br><a :href="`/files/i/${ internship.uuid }_fiche.pdf`" target="_blank">{{ internship.Student?.User?.name }}: studentenfiche</a>-->
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';

import { useStore } from '../../store.js';

const page = usePage();
const { education, internships } = storeToRefs(useStore());

const files = computed<RelatedFile[]>(() =>
  ((page.props.files as RelatedFile[]) ?? []).filter((file) => file.code.startsWith('place:'))
);
</script>
