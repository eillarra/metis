<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('planning') }}</h3>
    <div class="col"></div>
    <q-select
      v-model="selectedPeriod"
      :disable="!periodOptions.length"
      clearable
      dense
      rounded
      outlined
      :options="periodOptions"
      :label="$t('period')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedPeriod !== null ? 'blue-1' : 'white'"
    />
    <q-select
      v-model="selectedDiscipline"
      :disable="!disciplineOptions.length"
      clearable
      dense
      rounded
      outlined
      :options="disciplineOptions"
      :label="$t('discipline')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedDiscipline !== null ? 'blue-1' : 'white'"
    />
    <q-select
      v-model="selectedTrack"
      :disable="!trackOptions.length"
      clearable
      dense
      rounded
      outlined
      :options="trackOptions"
      :label="$t('track')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedTrack !== null ? 'blue-1' : 'white'"
    />
    <!--<date-range-filter v-model="selectedDateRange" class="col-6 col-md-2" />-->
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

import { useStore } from '../../store.js';

// import DateRangeFilter from '@/components/DateRangeFilter.vue';
import InternshipsCalendar from './InternshipsCalendar.vue';
import InternshipsTable from './InternshipsTable.vue';

const { internships } = storeToRefs(useStore());

const showTable = ref<boolean>(true);
const selectedBlock = ref<number | null>(null);
const selectedDateRange = ref<QuasarDateRange | null>(null);
const selectedDiscipline = ref<number | null>(null);
const selectedPeriod = ref<number | null>(null);
const selectedTrack = ref<number | null>(null);

const disciplineOptions = computed(() => {
  const ids: Set<number> = new Set();
  const disciplines: Discipline[] = [];

  internships.value.forEach((obj: Internship) => {
    if (obj.discipline && !ids.has(obj.discipline.id)) {
      ids.add(obj.discipline.id);
      disciplines.push(obj.discipline);
    }
  });

  disciplines.sort((a, b) => a.name.localeCompare(b.name));
  return disciplines.map((discipline) => ({ label: discipline.name, value: discipline.id }));
});

const periodOptions = computed(() => {
  const ids: Set<number> = new Set();
  const periods: Period[] = [];

  internships.value.forEach((obj: Internship) => {
    if (obj.period && !ids.has(obj.period.id)) {
      ids.add(obj.period.id);
      periods.push(obj.period);
    }
  });

  return periods.map((period) => ({
    label: `${period.program_internship.block?.name} / P${period.program_internship?.position}`,
    value: period.id,
  }));
});

const trackOptions = computed(() => {
  const ids: Set<number> = new Set();
  const tracks: TrackTiny[] = [];

  internships.value.forEach((obj: Internship) => {
    if (obj.track && !ids.has(obj.track.id)) {
      ids.add(obj.track.id);
      tracks.push(obj.track);
    }
  });

  return tracks.map((track) => ({ label: track.name, value: track.id }));
});

const filteredInternships = computed<Internship[]>(() => {
  return internships.value
    .filter((obj) => (selectedBlock.value ? obj.period.program_internship.block?.id === selectedBlock.value : true))
    .filter((obj) => (selectedPeriod.value ? obj.period?.id === selectedPeriod.value : true))
    .filter((obj) => (selectedDiscipline.value ? obj.discipline?.id === selectedDiscipline.value : true))
    .filter((obj) => (selectedTrack.value ? obj.track?.id === selectedTrack.value : true))
    .filter((obj) => {
      if (!selectedDateRange.value) return true;

      const start = new Date(obj.start_date);
      const end = new Date(obj.end_date);
      const filterStart = new Date(selectedDateRange.value.from);
      const filterEnd = new Date(selectedDateRange.value.to);

      return start.getTime() >= filterStart.getTime() && end.getTime() <= filterEnd.getTime();
    });
});
</script>
