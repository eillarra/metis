<template>
  <files-read-only-view v-if="project" :files="files">
    <template #title>
      <h3 class="text-ugent col-12 col-md-3 q-mb-lg">{{ $t('document', 9) }}</h3>
    </template>
  </files-read-only-view>
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

import FilesReadOnlyView from '@/components/rel/FilesReadOnlyView.vue';

const page = usePage();
const { education, project, internships } = storeToRefs(useStore());

const files = computed<RelatedFile[]>(() => page.props.files as RelatedFile[]);
</script>
