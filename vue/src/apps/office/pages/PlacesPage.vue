<template>
  <div class="row q-col-gutter-sm q-mb-sm">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('place', 9) }}</h3>
    <q-select
      dense
      square
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
  <places-table v-if="project" :places="filteredPlaces" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useOfficeStore } from '../store';

import PlacesTable from '../components/tables/PlacesTable.vue';

const { project, places } = storeToRefs(useOfficeStore());

const regionFilters = computed(() => {
  if (!places.value.length) {
    return [];
  }

  const regions: Region[] = [];

  places.value.forEach((place: Place) => {
    if (place.institution.region && !regions.find((region) => region.id === place.institution.region?.id)) {
      regions.push(place.institution.region);
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

const filteredPlaces = computed(() => {
  return places.value.filter((place) => !selectedRegion.value || place.institution.region?.id === selectedRegion.value);
});
</script>
