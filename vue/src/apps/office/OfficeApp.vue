<template>
  <div>
    <div class="row">
      <q-select
        v-if="projects.length"
        dense
        borderless
        square
        options-dense
        v-model="selectedProject"
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
import { computed, ComputedRef } from 'vue';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';

import { useOfficeStore } from './store';

const page = usePage();
const officeStore = useOfficeStore();

const djangoPrograms: ComputedRef<Program[]> = computed(() => page.props.programs);
const djangoProjects: ComputedRef<Project[]> = computed(() => page.props.projects);
const { projects, project, selectedProject } = storeToRefs(officeStore);

officeStore.setPrograms(djangoPrograms.value);
officeStore.setProjects(djangoProjects.value);
</script>
