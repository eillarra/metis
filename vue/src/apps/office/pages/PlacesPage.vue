<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('place', 9) }}</h3>
    <div class="col"></div>
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
    <q-select
      v-model="selectedRegion"
      :disable="!regionOptions.length"
      clearable
      dense
      rounded
      outlined
      :options="regionOptions"
      :label="$t('region')"
      options-dense
      emit-value
      map-options
      class="col-6 col-md-2"
      :bg-color="selectedRegion !== null ? 'blue-1' : 'white'"
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

import { useOfficeStore } from '../store';

import ProjectPlacesTable from '../components/tables/ProjectPlacesTable.vue';

const { project, projectPlaces } = storeToRefs(useOfficeStore());

const selectedDiscipline = ref<number | null>(null);
const selectedRegion = ref<number | null>(null);

const disciplineOptions = computed(() => {
  const ids: Set<number> = new Set();
  const disciplines: Discipline[] = [];

  projectPlaces.value.forEach((obj: ProjectPlace) => {
    obj.disciplines.forEach((discipline) => {
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

const regionOptions = computed(() => {
  const ids: Set<number> = new Set();
  const regions: Region[] = [];

  projectPlaces.value.forEach((obj: ProjectPlace) => {
    if (obj.place.region && !ids.has(obj.place.region.id)) {
      ids.add(obj.place.region.id);
      regions.push(obj.place.region);
    }
  });

  regions.sort((a, b) => a.name.localeCompare(b.name));
  return regions.map((region) => ({ label: region.name, value: region.id }));
});

const filteredPlaces = computed<ProjectPlace[]>(() => {
  // if selectedDiscipline is false, then fiter empty arrays of disciplines
  return projectPlaces.value
    .filter((obj) =>
      selectedDiscipline.value === 0
        ? !obj.disciplines.length
        : !selectedDiscipline.value || obj.disciplines.some((discipline) => discipline.id === selectedDiscipline.value)
    )
    .filter((obj) => !selectedRegion.value || obj.place.region?.id === selectedRegion.value);
});
</script>
