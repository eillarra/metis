<template>
  <div>
    <div class="row ugent__submenu">
      <q-select
        v-if="projects.length"
        dense
        borderless
        square
        options-dense
        v-model="selectedProjectId"
        :options="projects"
        option-value="id"
        option-label="name"
        emit-value
        map-options
        hide-bottom-space
        dropdown-icon="expand_more"
        class="ugent__submenu__select q-mb-lg"
        popup-content-class="q-menu__square"
      >
        <template #selected-item>
          <span class="text-underline">Stagebureau (project: {{ project?.name }})</span>
        </template>
      </q-select>
      <q-space />
      <!--<q-tabs class="ugent__submenu">
        <q-tab label="Dashboard" />
      </q-tabs>-->
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const officeStore = useStore();

const djangoEducation = computed<Education>(() => page.props.education as Education);
const djangoPrograms = computed<Program[]>(() => page.props.programs as Program[]);
const djangoProjects = computed<Project[]>(() => page.props.projects as Project[]);

const { projects, project, selectedProjectId } = storeToRefs(officeStore);

officeStore.setData(djangoEducation.value, djangoPrograms.value, djangoProjects.value);
</script>
