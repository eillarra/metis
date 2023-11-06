<template>
  <div>
    <div class="row ugent__submenu q-mb-lg">
      <div class="menu-item">
        <span>{{ $t('internship', 9) }} {{ education.short_name }}</span>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const store = useStore();

const education = ref<EducationTiny>(page.props.education as EducationTiny);

store.setData(
  page.props.education as EducationTiny,
  page.props.projects as Project[],
  page.props.students as Student[],
  page.props.project_place_options as ProjectPlaceOption[],
  page.props.internships as Internship[]
);
store.init();
</script>
