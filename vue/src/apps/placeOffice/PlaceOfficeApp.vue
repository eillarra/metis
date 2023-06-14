<template>
  <div>
    <div class="row ugent__submenu q-mb-lg">
      <div v-if="places.length == 1" class="menu-item">
        <span>Stageplaats {{ places[0].name }}</span>
      </div>
      <q-select
        v-else
        dense
        borderless
        square
        options-dense
        v-model="selectedPlaceId"
        :options="places"
        option-value="id"
        option-label="name"
        emit-value
        map-options
        hide-bottom-space
        dropdown-icon="expand_more"
        popup-content-class="q-menu__square"
      >
        <template #selected-item>
          <span class="text-underline">Stageplaats {{ (page.props.education as EducationTiny).short_name }}:
          {{ (page.props.place as Place).name }}</span>
        </template>
      </q-select>
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const store = useStore();

const selectedPlaceId = ref<number>((page.props.place as Place).id);
const places = computed<ContactPlace[]>(() => page.props.places as ContactPlace[]);

store.setData(
  page.props.education as EducationTiny,
  page.props.place as Place,
  (page.props.django_user as DjangoAuthenticatedUser).id
);

watch(
  () => selectedPlaceId.value,
  (id) => {
    window.location.href = `../${id}/`;
  }
);
</script>
