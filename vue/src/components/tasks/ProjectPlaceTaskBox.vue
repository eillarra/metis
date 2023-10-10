<template>
  <div v-if="activeQuestionings">
    {{ $t('tasks.intro', { email: education.office_email }) }}
    <div class="q-gutter-y-sm q-mt-md">
      <q-banner
        v-for="questioning in activeQuestionings"
        :key="questioning.id"
        :inline-actions="$q.screen.gt.sm"
        class="bg-yellow-3"
      >
        <template #default>
          <div class="text-body1 q-py-xs">
            <span v-if="questioning.form_definition.description">{{
              questioning.form_definition.description[locale]
            }}</span>
            <span v-else>{{ $t(`tasks.place.${questioning.type}.text`, { project_name: project.name }) }}</span
            ><br />
            <em>Deadline: {{ formatDate(questioning.end_at) }}</em>
          </div>
        </template>
        <template #action>
          <q-spinner v-if="!dataLoaded" color="yellow" size="2em" />
          <q-btn v-else @click="openQuestioning(questioning)" outline square color="ugent" :label="$t(`form.update`)" />
        </template>
      </q-banner>
    </div>
    <q-dialog v-if="selectedQuestioning && formDataResponses" v-model="dialogForm">
      <custom-form
        v-if="selectedQuestioning.type == 'project_place_information'"
        v-model="formDataResponses"
        :api-endpoint="projectPlace.rel_form_responses"
        :questioning="selectedQuestioning"
        :subtitle="projectPlace.Place?.name"
      />
      <project-place-availability-form v-else :project="project" />
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { formatDate } from '@/utils';

import TaskBox from './TaskBox.vue';
import ProjectPlaceAvailabilityForm from '@/components/custom_forms/ProjectPlaceAvailabilityForm.vue';
import CustomForm from '@/components/custom_forms/CustomForm.vue';

const props = defineProps<{
  education: EducationTiny;
  project: Project;
  projectPlace: ProjectPlaceTiny;
  activeQuestionings: Questioning[];
}>();

const { locale } = useI18n();

const dataLoaded = ref<boolean>(false);
const dialogForm = ref<boolean>(false);

const selectedQuestioning = ref<Questioning>();
const formDataResponses = ref<CustomFormResponse[]>();

function openQuestioning(questioning: Questioning) {
  selectedQuestioning.value = questioning;
  dialogForm.value = true;
}

onMounted(() => {
  api.get(props.projectPlace.rel_form_responses).then((response) => {
    formDataResponses.value = response.data;
    dataLoaded.value = true;
  });
});
</script>
