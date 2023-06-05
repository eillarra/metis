<template>
  <dialog-form icon="add" :title="$t('internship')">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive>
        <q-step :name="1" :title="$t('form.internship.create.new')" icon="edit">
          <div class="q-gutter-sm">
            <q-input v-model="projectName" dense :label="$t('project')" readonly />
            <api-autocomplete
              v-model="obj.ProjectPlace"
              clearable
              :data-source="(project as Project).rel_places"
              :mapper="placeMapper"
              :label="$t('place')"
            />
            <api-autocomplete
              v-model="obj.Student"
              clearable
              :data-source="projectStudents"
              :mapper="studentMapper"
              :label="$t('student')"
            />
            <period-select v-model="obj.period" :periods="filteredPeriods" :label="$t('period')" />
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
          :disable="!obj.ProjectPlace || !obj.Student || !obj.discipline"
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
import PeriodSelect from '../../components/PeriodSelect.vue';

const emit = defineEmits(['create:obj']);

const { t } = useI18n();
const store = useStore();
const { education, project, projectStudents } = storeToRefs(store);

const step = ref(1);
const obj = ref({
  project_place: null as number | null,
  student: null as number | null,
  period: null as number | null,
  discipline: null as number | null,
  Student: null as Student | null,
  ProjectPlace: null as ProjectPlace | null,
});
const projectName = computed<string>(() => (project.value ? project.value.name : ''));

const filteredPeriods = computed(() => {
  if (!project.value) return [];
  if (!obj.value.Student?.Track) return project.value.periods;

  return project.value.periods.filter((period) => {
    return (
      obj.value.Student?.Block?.id == period.ProgramInternship?.block &&
      obj.value.Student?.Track?.program_internships.includes(period.program_internship)
    );
  });
});

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
  return data.map((obj) => {
    const student: Student = obj as Student;
    return {
      id: student.id,
      name: (student.User as StudentUser).name,
      caption: `${student.Project?.name}-${student.Block?.name} / ${student.User?.email}`,
      Track: student.Track,
      Block: student.Block,
    };
  });
}

function createInternship() {
  api
    .post((project.value as Project).rel_internships, {
      student: obj.value.Student?.id,
      project_place: obj.value.ProjectPlace?.id,
      period: obj.value.period,
      track: obj.value.Student?.Track?.id,
      discipline: obj.value.discipline,
    })
    .then((res) => {
      store.createObj('projectInternship', res.data);
      notify.success(t('form.internship.create.success'));
      emit('create:obj');
    });
}
</script>
