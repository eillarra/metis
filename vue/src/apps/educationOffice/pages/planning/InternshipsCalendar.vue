<template>
  <h2>CALENDAR</h2>
  {{ internships }}
  <internship-form :obj="null" />
</template>

<script setup lang="ts">
import { toRefs } from 'vue';

import InternshipForm from './InternshipForm.vue';

const props = defineProps<{
  internships: Internship[];
}>();

const { internships } = toRefs(props);
</script>
