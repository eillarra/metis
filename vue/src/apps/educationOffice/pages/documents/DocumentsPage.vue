<template>
  <files-view v-if="project" :api-endpoint="project.rel_files" :visibility-options="['place', 'student']">
    <template #title>
      <h3 class="text-ugent col-12 col-md-3 q-mb-lg">{{ $t('document', 9) }}</h3>
    </template>
  </files-view>
  <q-separator class="q-my-lg" />
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">{{ $t('document', 9) }} (oud)</h4>
  </div>
  <ul>
    <li v-for="period in filteredPeriods" :key="period.id">
      <div>
        <span>{{ period.full_name }}</span
        >:&nbsp;
        <a :href="`./files/p/${period.id}/project_place_information.pdf`" target="_blank">Infofiches</a>&nbsp;|&nbsp;
        <a :href="`./files/p/${period.id}/student_information.pdf`">Student information</a>&nbsp;|&nbsp;
        <a :href="`./files/p/${period.id}/student_tops.xlxs`">Student tops (Excel)</a>
      </div>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import FilesView from '@/components/rel/FilesView.vue';

const { programs, project } = storeToRefs(useStore());

const programInternshipsToSkip = computed<Set<number>>(() => {
  const ids: Set<number> = new Set();
  programs.value.forEach((program: Program) => {
    program.tracks.forEach((track) => {
      if (track.name.includes('B')) {
        track.program_internships.forEach((period_id) => {
          if (ids.has(period_id)) {
            return;
          }
          ids.add(period_id);
        });
      }
    });
  });
  return ids;
});

const filteredPeriods = computed<Period[]>(() => {
  if (!project.value) return [];
  const ids = programInternshipsToSkip.value;
  return project.value.periods.filter((period) => !ids.has(period.program_internship));
});
</script>
