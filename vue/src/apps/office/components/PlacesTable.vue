<template>
  <data-table
    :title="$t('place', 10)"
    :loading="loading"
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    sort-by="name"
  >
    <template #filters>
      <q-select
        dense
        square
        outlined
        v-model="selectedRegion"
        :options="regionFilters"
        label="Filter regions"
        clearable
        options-dense
        emit-value
        map-options
        class="col-12 col-md-3"
      >
        <template #prepend>
          <q-icon name="filter_alt" />
        </template>
      </q-select>
    </template>
  </data-table>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, toRefs, watch, Ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { groupBy } from 'lodash-es';

import { api } from '@/axios.ts';
import DataTable from '@/components/DataTable.vue';

const { t } = useI18n();

const props = defineProps<{
  project: Project;
  programs: Program[] | null;
}>();

const loading: Ref<boolean> = ref(true);
const { project } = toRefs(props);
const places: Ref<Place[]> = ref([]);
const queryColumns = ['name', 'region'];

const regionFilters = computed(() => {
  if (!places.value.length) {
    return [];
  }

  const regions: Region[] = [];

  places.value.forEach((place: Place) => {
    if (place.region && !regions.find((region) => region.id === place.region.id)) {
      regions.push(place.region);
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

const selectedRegion: Ref<number | null> = ref(null);

async function fetchPlaces() {
  loading.value = true;
  places.value = [];

  await api
    .get(project.value.rel_places)
    .then((response) => {
      places.value = response.data;
    })
    .finally(() => {
      loading.value = false;
    });
}

const columns = [
  {
    name: 'name',
    field: 'name',
    required: true,
    label: t('field.name'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'region',
    field: 'region',
    label: t('field.region'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
  },
  {
    name: 'type',
    field: 'type',
    label: t('field.place_type'),
    align: 'left',
  },
  {
    name: 'disciplines',
    field: 'disciplines',
    label: t('field.disciplines'),
    align: 'left',
  },
];

const rows = computed(() => {
  return places.value
    .filter((place) => !selectedRegion.value || (place.region && place.region.id === selectedRegion.value))
    .map((place) => ({
      name: place.name,
      region: place.region ? place.region.name : null,
      type: place.type,
      disciplines: place.disciplines.map((discipline) => discipline.code).join(', '),
    }));
});

onMounted(() => {
  fetchPlaces();
});

watch(project, fetchPlaces);
</script>
