<template>
  <div class="q-mb-xl">
    <h3 class="text-ugent col-12 col-md-3 q-mb-lg">{{ $t('my_tasks') }}</h3>
    <div v-if="userIsAdmin && internshipsWithoutMentors.length">
      - {{ $t('tasks.place.internships_missing_mentors.text', { count: internshipsWithoutMentors.length }) }}
      <router-link :to="{ name: 'planning' }">{{
        $t('tasks.place.internships_missing_mentors.btn_label')
      }}</router-link>
    </div>
    <div v-if="userIsAdmin && internshipsNotApproved.length">
      - {{ $t('tasks.place.internships_not_approved.text', { count: internshipsNotApproved.length }) }}
      <router-link :to="{ name: 'planning' }">{{ $t('tasks.place.internships_not_approved.btn_label') }}</router-link>
    </div>
    <project-place-task-box
      v-if="userIsAdmin && activeQuestionings.length"
      :education="(education as EducationTiny)"
      :project="(project as ProjectTiny)"
      :project-place="(projectPlace as ProjectPlaceTiny)"
      :active-questionings="(activeQuestionings as Questioning[])"
      class="q-mb-lg"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import ProjectPlaceTaskBox from '@/components/tasks/ProjectPlaceTaskBox.vue';

const { education, place, userIsAdmin, activeQuestionings, project, projectPlace, internships } = storeToRefs(
  useStore()
);

// NEW VERSION

const internshipsWithoutMentors = computed<Internship[]>(() => {
  return (internships.value as Internship[]).filter((internship) => !internship.mentors.length);
});

const internshipsNotApproved = computed<Internship[]>(() => {
  return (internships.value as Internship[]).filter((internship) => !internship.is_approved);
});
</script>
