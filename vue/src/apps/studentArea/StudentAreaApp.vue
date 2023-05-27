<template>
  <div>
    <div class="row ugent__submenu q-mb-lg">
      <div class="menu-item">
        <span>{{ $t('internship', 9) }} {{ djangoEducation.short_name }}</span>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

import { useStore } from './store';

const page = usePage();
const store = useStore();

const djangoEducation = computed<EducationTiny>(() => page.props.education as EducationTiny);
const djangoStudents = computed<Student[]>(() => page.props.student_set as Student[]);

store.setData(djangoEducation.value, djangoStudents.value);
store.init();
</script>
