<template>
  <div v-if="activeDates">
    {{ $t('tasks.intro', { email: education.office_email }) }}
    <div class="q-gutter-y-sm q-mt-md">
      <q-banner v-for="date in activeDates" :key="date.id" :inline-actions="$q.screen.gt.sm" class="bg-yellow-3">
        <template #default>
          <div class="text-body1 q-py-xs">
            {{ $t(`tasks.place.${date.type}.text`, { project_name: project.name }) }}<br />
            <em>Deadline: {{ formatDate(date.end_at) }}</em>
          </div>
        </template>
        <template #action>
          <q-spinner v-if="!dataLoaded" color="yellow" size="2em" />
          <q-btn
            v-else
            @click="openForm(date.form)"
            outline
            square
            color="ugent"
            :label="$t(`tasks.place.${date.type}.btn_label`)"
          />
        </template>
      </q-banner>
    </div>
    <q-dialog v-model="dialogForm">
      <custom-form
        v-if="selectedForm && formDataResponses"
        v-model="formDataResponses"
        :api-endpoint="projectPlace.rel_form_responses"
        :form="selectedForm"
      />
      <project-place-availability-form v-else :project="project" />
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import { api } from '@/axios';
import { formatDate } from '@/utils';

import CustomForm from '@/components/forms/CustomForm.vue';
import ProjectPlaceAvailabilityForm from './ProjectPlaceAvailabilityForm.vue';

const props = defineProps<{
  education: EducationTiny;
  project: Project;
  projectPlace: ProjectPlaceTiny;
}>();

const dataLoaded = ref<boolean>(false);
const dialogForm = ref<boolean>(false);
const activeDates = computed<ImportantDate[]>(() => {
  return props.project.important_dates.filter((date) => date.is_active);
});

const selectedForm = ref<CustomForm>();
const formDataResponses = ref<CustomFormResponse[]>();

function openForm(form?: CustomForm) {
  selectedForm.value = form;
  dialogForm.value = true;
}

onMounted(() => {
  api.get(props.projectPlace.rel_form_responses).then((response) => {
    formDataResponses.value = response.data;
    dataLoaded.value = true;
  });
});
</script>
