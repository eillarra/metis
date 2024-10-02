<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none use-default-q-btn">
      {{ $t('place', 9) }}
      <a v-show="projectPlaces.length" :href="placesExcelPath" target="_blank">
        <q-btn round outline :icon="iconDownload" size="sm" color="primary" class="q-ml-md q-pa-xs">
          <q-tooltip :delay="250">{{ $t('download.excel') }}</q-tooltip>
        </q-btn>
      </a>
    </h3>
    <div class="col"></div>
    <period-select
      as-filter
      :label="$t('availability')"
      :periods="periodOptions"
      v-model="selectedPeriod"
      class="col-6 col-md-2"
    />
    <place-option-select
      v-if="education?.place_locations.length"
      as-filter
      :label="$t('place_location')"
      :place-types="(education?.place_locations as PlaceLocation[])"
      v-model="selectedPlaceLocation"
      class="col-6 col-md-2"
    />
    <place-option-select
      v-if="education?.place_types.length"
      as-filter
      :label="$t('place_type')"
      :place-types="(education?.place_types as PlaceType[])"
      v-model="selectedPlaceType"
      class="col-6 col-md-2"
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
    >
      <template #selected-item="scope">
        <span class="ellipsis">{{ scope.opt.label }}</span>
      </template>
    </q-select>
  </div>
  <project-places-table v-if="project" :project-places="filteredPlaces" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import PeriodSelect from '../../components/PeriodSelect.vue';
import PlaceOptionSelect from '../../components/PlaceOptionSelect.vue';
import ProjectPlacesTable from './ProjectPlacesTable.vue';

import { iconDownload } from '@/icons';

const { education, project, projectPlaces } = storeToRefs(useStore());

const selectedDiscipline = ref<number | null>(null);
const selectedPeriod = ref<number | null>(null);
const selectedPlaceLocation = ref<number | null>(null);
const selectedPlaceType = ref<number | null>(null);

const disciplineOptions = computed(() => {
  const ids: Set<number> = new Set();
  const disciplines: Discipline[] = [];

  projectPlaces.value.forEach((obj: ProjectPlace) => {
    (obj.Disciplines as Discipline[]).forEach((discipline) => {
      if (!ids.has(discipline.id)) {
        ids.add(discipline.id);
        disciplines.push(discipline);
      }
    });
  });

  disciplines.sort((a, b) => a.name.localeCompare(b.name));
  return [
    ...disciplines.map((discipline) => ({ label: discipline.name, value: discipline.id })),
    ...[
      {
        label: '-',
        value: 0,
      },
    ],
  ];
});

const periodOptions = computed(() => {
  const ids: Set<number> = new Set();

  // check availability_set for non zero periods
  projectPlaces.value.forEach((obj: ProjectPlace) => {
    if (obj.availability_set && obj.availability_set.length) {
      obj.availability_set.forEach((availability: ProjectPlaceAvailability) => {
        if (availability.period && availability.period) {
          ids.add(availability.period);
        }
      });
    }
  });

  // get full Period value from project
  const periods: Period[] = [];
  project.value?.periods.forEach((period: Period) => {
    if (ids.has(period.id)) {
      periods.push(period);
    }
  });

  return periods;
});

const filteredPlaces = computed<ProjectPlace[]>(() => {
  return projectPlaces.value
    .filter((obj) =>
      selectedDiscipline.value === 0
        ? !obj.disciplines.length
        : !selectedDiscipline.value || obj.disciplines.some((id: number) => id === selectedDiscipline.value)
    )
    .filter((obj) => !selectedPeriod.value || obj._periods.has(selectedPeriod.value))
    .filter((obj) => !selectedPlaceLocation.value || obj.place.location === selectedPlaceLocation.value)
    .filter((obj) => !selectedPlaceType.value || obj.place.type === selectedPlaceType.value);
});

const placesExcelPath = computed(() => {
  return `/nl/files/p/proj_${project.value?.id}_places.xlsx`;
});
</script>
