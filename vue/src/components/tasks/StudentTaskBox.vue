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
            Net zoals bij de stageverdeling in 3e bachelor, kunnen jullie voorkeursplaatsen doorgeven.<br />
            <em>Deadline: {{ formatDate(questioning.end_at) }}</em>
          </div>
        </template>
        <template #action>
          <q-spinner v-if="!dataLoaded" color="yellow" size="2em" />
          <q-btn v-else @click="openQuestioning(questioning)" outline square color="ugent" label="Tops bijwerken" />
        </template>
      </q-banner>
    </div>
    <q-dialog v-if="selectedQuestioning && formDataResponses" v-model="dialogQuestioning">
      <tops-form
        v-if="selectedQuestioning.code == 'student_tops'"
        v-model="formDataResponses"
        :api-endpoint="student.rel_form_responses"
        :questioning="(selectedQuestioning as Questioning)"
        :project-place-options="props.projectPlaceOptions"
        :skip-place-id="props.skipPlaceId"
      />
      <custom-form
        v-else
        v-model="formDataResponses"
        :api-endpoint="student.rel_form_responses"
        :questioning="(selectedQuestioning as Questioning)"
        :addresses-api-endpoint="
          selectedQuestioning.code == 'student_information' ? props.addressesApiEndpoint : undefined
        "
      />
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

import { api } from '@/axios';
import { formatDate } from '@/utils';

import TaskBox from './TaskBox.vue';
import TopsForm from '@/components/custom_forms/TopsForm.vue';
import CustomForm from '@/components/custom_forms/CustomForm.vue';

const props = defineProps<{
  education: EducationTiny;
  project: Project;
  student: Student;
  activeQuestionings: Questioning[];
  addressesApiEndpoint?: ApiEndpoint;
  projectPlaceOptions?: ProjectPlace[];
  skipPlaceId?: number | null;
}>();

const dataLoaded = ref<boolean>(false);
const dialogQuestioning = ref<boolean>(false);

const selectedQuestioning = ref<CustomForm | TopsForm>();
const formDataResponses = ref<CustomFormResponse[]>();

function openQuestioning(questioning: Questioning) {
  selectedQuestioning.value = questioning;
  dialogQuestioning.value = true;
}

onMounted(() => {
  api.get(props.student.rel_form_responses).then((response) => {
    formDataResponses.value = response.data;
    dataLoaded.value = true;
  });
});
</script>
