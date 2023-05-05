<template>
  <div class="row q-col-gutter-sm q-mb-sm justify-between">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('planning') }}</h3>
    <program-block-filter v-if="project" :programs="programs" v-model="selectedBlock" class="col-12 col-md-2" />
    <q-btn-toggle
      v-show="false"
      v-model="showTable"
      flat
      round
      :options="[
        { slot: 'table', value: true },
        { slot: 'calendar', value: false },
      ]"
      class="q-pa-none"
    >
      <template #calendar>
        <q-icon name="today" />
      </template>
      <template #table>
        <q-icon name="tab" />
      </template>
    </q-btn-toggle>
  </div>
  <internships-table v-if="showTable" :internships="filteredInternships" />
  <internships-calendar v-else :internships="filteredInternships" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useOfficeStore } from '../store';

import InternshipsCalendar from '../components/InternshipsCalendar.vue';
import InternshipsTable from '../components/tables/InternshipsTable.vue';
import ProgramBlockFilter from '../components/ProgramBlockFilter.vue';

const { project, programs, internships } = storeToRefs(useOfficeStore());

const showTable = ref<boolean>(true);
const selectedBlock = ref<number | null>(null);

const filteredInternships = computed<Internship[]>(() => {
  return internships.value.filter((obj) =>
    selectedBlock.value ? obj.program_internship.block?.id === selectedBlock.value : true
  );
});
</script>
