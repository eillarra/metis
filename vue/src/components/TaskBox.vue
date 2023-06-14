<template>
  <div>
    <div v-if="activeDates">
      Er zijn taken die u nog moet uitvoeren voor {{ project.name }}:
      <div class="q-gutter-y-sm q-mt-md">
        <q-banner v-for="date in activeDates" :key="date.id" inline-actions class="bg-yellow-3">
          <template #default>
            <div class="text-body1 q-py-xs">
              {{ $t(`tasks.place.${date.type}.text`) }}<br />
              Deadline: {{ date.end_at }}
            </div>
          </template>
          <template #action>
            <q-spinner v-if="!dataLoaded" color="yellow" size="2em" />
            <q-btn
              v-else-if="date.form"
              @click="openForm(date.form)"
              outline
              square
              color="ugent"
              :label="$t(`tasks.place.${date.type}.btn_label`)"
            />
            <span v-else></span>
          </template>
        </q-banner>
      </div>
    </div>
    <div v-else>Er zijn geen taken die u nog moet uitvoeren voor {{ project.name }}.</div>
    <q-dialog v-model="dialogForm">
      <custom-form
        v-if="selectedForm && formDataResponses"
        v-model="formDataResponses"
        :api-endpoint="projectPlace.rel_form_responses"
        :form="selectedForm"
      />
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import { api } from '@/axios';

import CustomForm from '@/components/forms/CustomForm.vue';

const props = defineProps<{
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
