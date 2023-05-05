<template>
  <div class="row q-col-gutter-lg q-mt-lg">
    <div v-if="educations.length" class="col-12 col-md-3">
      <ugent-link-list title="Stagebureau" :items="links" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

import UgentLinkList from '@/components/UgentLinkList.vue';

const page = usePage();

const educations = computed<Education[]>(() => page.props.educations as Education[]);

const links = computed(() =>
  educations?.value.map((education) => ({
    label: education.short_name,
    href: education.url,
  }))
);
</script>
