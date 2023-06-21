<template>
  <div>
    <div class="row ugent__submenu q-mb-lg">
      <div v-if="djangoEducations.length < 2" class="menu-item">
        <span>Stagebureau {{ djangoEducation.short_name }}</span>
      </div>
      <q-select
        v-else
        dense
        borderless
        square
        options-dense
        v-model="selectedEducationId"
        :options="djangoEducations"
        option-value="code"
        option-label="short_name"
        emit-value
        map-options
        hide-bottom-space
        dropdown-icon="expand_more"
        popup-content-class="q-menu__square"
      >
        <template #selected-item>
          <span class="text-underline">Stagebureau {{ djangoEducation.short_name }}</span>
        </template>
      </q-select>
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
        popup-content-class="q-menu__square"
        class="q-ml-md"
      >
        <template #selected-item>
          <span class="text-underline">{{ project?.name }}</span>
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
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const route = useRoute();
const store = useStore();

const djangoEducations = computed<EducationTiny[]>(() => page.props.educations as EducationTiny[]);
const djangoEducation = computed<Education>(() => page.props.education as Education);
const djangoPrograms = computed<Program[]>(() => page.props.programs as Program[]);
const djangoProjects = computed<Project[]>(() => page.props.projects as Project[]);

const { projects, project, selectedProjectId } = storeToRefs(store);

store.setData(djangoEducation.value, djangoPrograms.value, djangoProjects.value);

const selectedEducationId = ref((page.props.education as Education).id);

watch(
  () => selectedEducationId.value,
  (code) => {
    window.location.href = `../${code}/#${route.path}`;
  }
);
</script>
