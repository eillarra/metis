<template>
  <dialog-form icon="add" :title="$t('internship')">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive>
        <q-step :name="1" :title="$t('form.internship.create.new')" icon="edit">
          <div class="q-gutter-sm">
            <q-input v-model="projectName" dense :label="$t('project')" readonly />
            <api-autocomplete
              v-model="obj.project_place"
              clearable
              :data-source="(project as Project).rel_places"
              :mapper="placeMapper"
              :label="$t('place')"
            />
            <api-autocomplete
              v-model="obj.student"
              clearable
              :data-source="students"
              :mapper="studentMapper"
              :label="$t('student')"
            />
            <discipline-select
              v-if="education"
              v-model="obj.discipline"
              :disciplines="education.disciplines"
              :label="$t('period')"
            />
            <discipline-select
              v-if="education"
              v-model="obj.discipline"
              :disciplines="education.disciplines"
              :label="$t('discipline')"
            />
          </div>
          <q-stepper-navigation class="flex"> </q-stepper-navigation>
        </q-step>
      </q-stepper>
    </template>
    <template #footer>
      <div class="flex q-gutter-sm q-pa-lg">
        <q-space />
        <q-btn
          unelevated
          @click="createInternship"
          color="ugent"
          :label="$t('form.add_to_project')"
          :disable="!obj.project_place || !obj.student || !obj.discipline || obj.period"
        />
      </div>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import ApiAutocomplete from '@/components/forms/ApiAutocomplete.vue';
import DialogForm from '@/components/forms/DialogForm.vue';
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';

const emit = defineEmits(['create:obj']);

const { t } = useI18n();
const officeStore = useStore();
const { education, project, students } = storeToRefs(officeStore);

const step = ref(1);
const obj = ref({
  project_place: null as ProjectPlace | null,
  student: null as Student | null,
  discipline: null as Discipline | null,
});
const projectName = computed<string>(() => (project.value ? project.value.name : ''));

function placeMapper(data: ApiObject[]) {
  return data.map((obj) => {
    const place: Place = (obj as ProjectPlace).place;
    return {
      id: obj.id,
      name: place.name,
      caption: `${place.type} / ${place.region?.name}`,
    };
  });
}

function studentMapper(data: ApiObject[]) {
  return data.map((obj) => ({
    id: obj.id,
    name: (obj as Student).name,
    caption: (obj as Student).email,
  }));
}

function createInternship() {
  api
    .post(project.value?.rel_internships, {
      student: obj.value.student?.id,
      project_place: obj.value.project_place?.id,
      discipline_id: obj.value.discipline?.id,
    })
    .then((res) => {
      officeStore.createObj('projectInternship', res.data);
      notify.success(t('form.internship.create.saved'));
      emit('create:obj');
    });
}
</script>
