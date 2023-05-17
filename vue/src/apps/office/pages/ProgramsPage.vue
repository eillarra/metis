<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('program', 9) }}</h3>
    <div class="col"></div>
  </div>
  <div class="row q-col-gutter-md">
    <div v-for="program in programs" :key="program.id" class="col-12 col-md-4">
      Name: {{ program.name }}<br />
      Blocks:
      <ul>
        <li v-for="block in program.blocks" :key="block.id">
          Block {{ block.name }}
          <ul>
            <li v-for="internship in block.internships" :key="internship.id">Internship {{ internship.name }}</li>
          </ul>
        </li>
      </ul>
      Tracks:
      <ul v-if="program.tracks.length">
        <li v-for="track in program.tracks" :key="track.id">
          Track {{ track.name }}
          <ul>
            <li v-for="internship in track.program_internships" :key="internship">
              Internship {{ internshipMap.get(internship).name }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';

import { useOfficeStore } from '../store';

const { programs } = storeToRefs(useOfficeStore());

const internshipMap = computed<Map<number, ProgramInternship>>(() => {
  let map = new Map();

  programs.value.forEach((program) => {
    program.blocks.forEach((block) => {
      block.internships.forEach((internship: ProgramInternship) => {
        map.set(internship.id, internship);
      });
    });
  });

  return map;
});
</script>
