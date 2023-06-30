<template>
  <div v-if="activeDates">
    {{ $t('tasks.intro', { email: education.office_email }) }}
    <div class="q-gutter-y-sm q-mt-md">
      <q-banner v-for="date in activeDates" :key="date.id" :inline-actions="$q.screen.gt.sm" class="bg-yellow-3">
        <template #default>
          <div class="text-body1 q-py-xs">
            Net zoals bij de stageverdeling in 3e bachelor, kunnen jullie voorkeursplaatsen doorgeven.<br />
            <em>Deadline: {{ formatDate(date.end_at) }}</em>
          </div>
        </template>
        <template #action>
          <q-spinner v-if="!dataLoaded" color="yellow" size="2em" />
          <q-btn v-else @click="openForm(date.form)" outline square color="ugent" label="Tops bijwerken" />
        </template>
      </q-banner>
    </div>
    <q-dialog v-if="selectedForm && formDataResponses" v-model="dialogForm">
      <tops-form
        v-if="selectedForm.code == 'student_tops'"
        v-model="formDataResponses"
        :api-endpoint="student.rel_form_responses"
        :form="(selectedForm as TopsForm)"
        :project-place-options="props.projectPlaceOptions"
        :skip-place-id="props.skipPlaceId"
      />
      <custom-form
        v-else
        v-model="formDataResponses"
        :api-endpoint="student.rel_form_responses"
        :form="(selectedForm as CustomForm)"
        :addresses-api-endpoint="selectedForm.code == 'student_information' ? props.addressesApiEndpoint : undefined"
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
  activeDates: ImportantDate[];
  addressesApiEndpoint?: ApiEndpoint;
  projectPlaceOptions?: ProjectPlace[];
  skipPlaceId?: number | null;
}>();

const dataLoaded = ref<boolean>(false);
const dialogForm = ref<boolean>(false);

const selectedForm = ref<CustomForm | TopsForm>();
const formDataResponses = ref<CustomFormResponse[]>();

function openForm(form?: CustomForm | TopsForm) {
  selectedForm.value = form;
  dialogForm.value = true;
}

onMounted(() => {
  api.get(props.student.rel_form_responses).then((response) => {
    formDataResponses.value = response.data;
    dataLoaded.value = true;
  });
});
</script>
