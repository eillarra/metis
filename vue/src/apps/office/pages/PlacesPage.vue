<template>
  <div class="row q-col-gutter-sm q-mb-sm justify-between">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('place', 9) }}</h3>
    <q-select
      dense
      square
      oulined
      v-model="selectedRegion"
      :options="regionFilters"
      :label="$t('region')"
      clearable
      options-dense
      emit-value
      map-options
      class="col-12 col-md-2"
    >
      <template #prepend>
        <q-icon name="filter_alt" />
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

const regionFilters = computed(() => {
  if (!projectPlaces.value.length) {
    return [];
  }

  const regions: Region[] = [];

  projectPlaces.value.forEach((obj: ProjectPlace) => {
    if (obj.place.region && !regions.find((region) => region.id === obj.place.region?.id)) {
      regions.push(obj.place.region);
    }
  });

  return regions
    .map((region: Region) => {
      return {
        label: region.name,
        value: region.id,
      };
    })
    .sort((a: { label: string }, b: { label: string }) => a.label.localeCompare(b.label));
});

const selectedRegion = ref<number | null>(null);

const filteredPlaces = computed<ProjectPlace[]>(() => {
  return projectPlaces.value.filter((obj) => !selectedRegion.value || obj.place.region?.id === selectedRegion.value);
});
</script>
