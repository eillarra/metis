<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('student', 9) }}</h3>
    <div class="col"></div>
    <program-block-select
      v-if="project"
      as-filter
      :programs="programs"
      v-model="selectedBlock"
      class="col-12 col-md-2"
    />
    <track-select v-if="project" as-filter :programs="programs" v-model="selectedTrack" class="col-12 col-md-2" />
  </div>
  <students-table v-if="project" :students="filteredStudents" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import ProgramBlockSelect from '../../components/ProgramBlockSelect.vue';
import TrackSelect from '../../components/TrackSelect.vue';
import StudentsTable from './StudentsTable.vue';

const { project, programs, students } = storeToRefs(useStore());

const selectedBlock = ref<number | null>(null);
const selectedTrack = ref<number | null>(null);

const filteredStudents = computed<StudentUser[]>(() => {
  return students.value
    .filter((user) =>
      selectedBlock.value
        ? user.student_set.some(
            (student) => student.project == project.value?.id && student.block == selectedBlock.value
          )
        : user.student_set.some((student) => student.project == project.value?.id)
    )
    .filter((user) =>
      selectedTrack.value ? user.student_set.some((student) => student.track == selectedTrack.value) : true
    );
});
</script>
