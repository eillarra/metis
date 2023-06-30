<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('document', 9) }}</h3>
  </div>
  <h4>{{ $t('place', 9) }}: infofiche</h4>
  <q-list dense>
    <q-item v-for="period in filteredPeriods" :id="period.id">
      <a :href="`./files/p/${period.id}/project_place_information.pdf`" target="_blank"
        >{{ period.ProgramInternship?.Block?.name }} / P{{ period.name }}</a
      >
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

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
  const ids = programInternshipsToSkip.value;
  return project.value.periods.filter((period) => !ids.has(period.program_internship));
});
</script>
