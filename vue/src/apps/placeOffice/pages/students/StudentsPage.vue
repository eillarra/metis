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
  </div>
  <students-table v-if="project" :students="filteredStudents" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import StudentsTable from './StudentsTable.vue';

/*const { project, programs, students } = storeToRefs(usestore());

const selectedBlock = ref<number | null>(null);

const filteredStudents = computed<Student[]>(() => {
  return students.value.filter((user) =>
    selectedBlock.value
      ? user.student_set.some((rec) => rec.project.id == project.value?.id && rec.block.id == selectedBlock.value)
      : user.student_set.some((rec) => rec.project.id == project.value?.id)
  );
});*/
</script>
