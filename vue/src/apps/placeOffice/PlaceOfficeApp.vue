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
        :dropdown-icon="$q.iconSet.expansionItem.icon"
        popup-content-class="q-menu__square"
      >
        <template #selected-item>
          <span class="text-underline"
            >Stageplaats {{ (page.props.education as EducationTiny).short_name }}:
            {{ (page.props.place as Place).name }}</span
          >
        </template>
      </q-select>
      <div v-if="availableProjects.length" class="menu-item q-ml-md">
        <span>{{ availableProjects[0].label }}</span>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const route = useRoute();
const store = useStore();

const { availableProjects } = storeToRefs(store);

const selectedPlaceId = ref<number>((page.props.place as Place).id);
const places = computed<ContactPlace[]>(() => page.props.contact_places as ContactPlace[]);

store.setData(
  page.props.education as EducationTiny,
  page.props.projects as Project[],
  page.props.place as Place,
  page.props.project_places as ProjectPlaceTiny[],
  page.props.internships as Internship[],
  (page.props.django_user as DjangoAuthenticatedUser).id,
);

watch(
  () => selectedPlaceId.value,
  (id) => {
    window.location.href = `../${id}/#${route.path}`;
  },
);
</script>
