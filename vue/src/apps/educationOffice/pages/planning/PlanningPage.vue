<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none use-default-q-btn">
      {{ $t('allocation') }}
      <q-btn
        v-if="internships.length"
        round
        outline
        :href="projectExcelPath"
        target="_blank"
        :icon="iconDownload"
        size="sm"
        color="primary"
        class="q-ml-md q-pa-xs"
      >
        <q-tooltip :delay="250">{{ $t('download.excel') }}</q-tooltip>
      </q-btn>
    </h3>
    <div class="col"></div>
    <period-select
      as-filter
      v-show="periodOptions.length > 1"
      v-model="selectedPeriod"
      :periods="periodOptions"
      class="col-6 col-md-2"
    />
    <q-select
      v-show="statusOptions.length > 1"
      v-model="selectedStatus"
      :options="statusOptions"
      clearable
      dense
      rounded
      outlined
      :label="$t('field.status')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedStatus !== null ? 'blue-1' : 'white'"
    />
    <q-select
      v-show="disciplineOptions.length > 1"
      v-model="selectedDiscipline"
      :options="disciplineOptions"
      clearable
      dense
      rounded
      outlined
      :label="$t('discipline')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedDiscipline !== null ? 'blue-1' : 'white'"
    />
    <track-select
      as-filter
      v-show="programs.length > 1"
      v-model="selectedTrack"
      :programs="programs"
      class="col-6 col-md-2"
    />
    <date-range-filter v-model="selectedDateRange" class="col-6 col-md-2" />
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
import { useI18n } from 'vue-i18n';

import { useStore } from '../../store.js';

import DateRangeFilter from '@/components/DateRangeFilter.vue';
import PeriodSelect from '../../components/PeriodSelect.vue';
import TrackSelect from '../../components/TrackSelect.vue';
import InternshipsCalendar from './InternshipsCalendar.vue';
import InternshipsTable from './InternshipsTable.vue';

import { iconDownload } from '@/icons';

const { t } = useI18n();
const { project, programs, internships } = storeToRefs(useStore());

const showTable = ref<boolean>(true);
const selectedBlock = ref<number | null>(null);
const selectedDateRange = ref<QuasarDateRange | null>(null);
const selectedDiscipline = ref<number | null>(null);
const selectedPeriod = ref<number | null>(null);
const selectedStatus = ref<string | null>(null);
const selectedTrack = ref<number | null>(null);

const statusLabels = {
  preplanning: t('internship_status.preplanning'),
  concept: t('internship_status.concept'),
  definitive: t('internship_status.definitive'),
  cancelled: t('internship_status.cancelled'),
  unsuccessful: t('internship_status.unsuccessful'),
};

const projectExcelPath = computed(() => {
  return `/nl/files/p/proj_${project.value?.id}_planning.xlsx`;
});

const disciplineOptions = computed(() => {
  const ids: Set<number> = new Set();
  const disciplines: Discipline[] = [];

  internships.value.forEach((obj: Internship) => {
    if (obj.discipline && !ids.has(obj.discipline)) {
      ids.add(obj.discipline);
      disciplines.push(obj.Discipline as Discipline);
    }
  });

  disciplines.sort((a, b) => a.name.localeCompare(b.name));
  return disciplines.map((discipline) => ({ label: discipline.name, value: discipline.id }));
});

const periodOptions = computed(() => {
  const ids: Set<number> = new Set();
  const periods: Period[] = [];

  internships.value.forEach((obj: Internship) => {
    if (obj.period && !ids.has(obj.period)) {
      ids.add(obj.period);
      periods.push(obj.Period as Period);
    }
  });

  return periods;
});

const statusOptions = computed<QuasarSelectOption[]>(() => {
  const ids: Set<string> = new Set();
  const options: QuasarSelectOption[] = [];

  internships.value.forEach((obj: Internship) => {
    if (obj.status && !ids.has(obj.status)) {
      options.push({
        label: statusLabels[obj.status as keyof typeof statusLabels] || obj.status,
        value: obj.status,
      } as QuasarSelectOption);
      ids.add(obj.status);
    }
  });

  return options;
});

const filteredInternships = computed<Internship[]>(() => {
  return internships.value
    .filter((obj) => (selectedBlock.value ? obj.Period?.ProgramInternship?.block === selectedBlock.value : true))
    .filter((obj) => (selectedPeriod.value ? obj.period === selectedPeriod.value : true))
    .filter((obj) => (selectedDiscipline.value ? obj.discipline === selectedDiscipline.value : true))
    .filter((obj) => (selectedStatus.value ? obj.status === selectedStatus.value : true))
    .filter((obj) => (selectedTrack.value ? obj.track === selectedTrack.value : true))
    .filter((obj) => {
      if (!selectedDateRange.value) return true;

      const start = new Date(obj.start_date);
      const filterStart = new Date(selectedDateRange.value.from);
      const filterEnd = new Date(selectedDateRange.value.to);

      return start.getTime() >= filterStart.getTime() && start.getTime() <= filterEnd.getTime();
    });
});
</script>
