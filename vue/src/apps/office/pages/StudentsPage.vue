<template>
  <students-table v-if="project" :project="project" :programs="programs" />
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useOfficeStore } from '../store';

import StudentsTable from '../components/StudentsTable.vue';

const officeStore = useOfficeStore();

const { project, programs } = storeToRefs(officeStore);
</script>
