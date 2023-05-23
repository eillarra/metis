<template>
  <div>
    <div class="row ugent__submenu q-mb-lg">
      <div class="menu-item">
        <span>{{ $t('internship', 9) }} {{ djangoEducation.short_name }}</span>
      </div>
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
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const officeStore = useStore();

const djangoEducation = computed<EducationTiny>(() => page.props.education as EducationTiny);
const djangoProjectStudents = computed<ProjectStudent[]>(() => page.props.student_set as ProjectStudent[]);

officeStore.setData(djangoEducation.value, djangoProjectStudents.value);
</script>
