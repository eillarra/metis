<template>
  <dialog-form :icon="iconAdd" :title="$t('student')">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" :title="$t('form.student.create.add_existing')" :icon="iconSearch" :active-icon="iconSearch">
          {{ $t('form.student.create.search') }}
          <div class="q-gutter-sm q-mt-sm">
            <readonly-field v-if="project" :label="$t('project')" :value="project.name" class="col-12 col-md" />
            <div class="row q-col-gutter-lg q-pt-sm q-pl-sm">
              <track-select :programs="programs" v-model="formData.track" class="col-12 col-md" />
              <program-block-select :programs="programs" v-model="formData.block" class="col-12 col-md" />
            </div>
            <api-autocomplete
              v-model="formData.user"
              clearable
              data-source="/users/"
              :mapper="userMapper"
              :label="$t('student')"
            />
            <q-input v-model="formData.number" dense :label="$t('field.student_number')" type="text" />
          </div>
          <q-stepper-navigation class="flex">
            <q-btn
              unelevated
              @click="step = 2"
              color="blue-1"
              text-color="ugent"
              :label="$t('form.skip')"
              :disable="!!formData.user"
            />
            <q-space />
            <q-btn
              unelevated
              @click="addStudent"
              color="ugent"
              :label="$t('form.add_to_project')"
              :disable="!formData.user || !formData.block"
            />
          </q-stepper-navigation>
        </q-step>
        <q-step :name="2" :title="$t('form.student.create.new')" :icon="iconEmail" :active-icon="iconEmail">
          {{ $t('form.student.create.invite') }}
          <div class="q-gutter-sm q-mt-sm">
            <readonly-field v-if="project" :label="$t('project')" :value="project.name" class="col-12 col-md" />
            <div class="row q-col-gutter-lg q-pt-sm q-pl-sm">
              <track-select :programs="programs" v-model="formData.track" class="col-12 col-md" />
              <program-block-select :programs="programs" v-model="formData.block" class="col-12 col-md" />
            </div>
            <q-input v-model="formData.name" dense :label="$t('field.name')" type="text" />
            <q-input v-model="formData.email" dense :label="$t('field.email')" type="email" />
            <q-input v-model="formData.number" dense :label="$t('field.student_number')" type="text" />
          </div>
        </q-step>
      </q-stepper>
    </template>
    <template #footer>
      <div v-if="step == 2" class="flex q-gutter-sm q-pa-lg">
        <q-btn unelevated @click="step = 1" color="blue-1" text-color="ugent" :label="$t('form.back')" />
        <q-space />
        <q-btn
          unelevated
          @click="createStudent"
          color="ugent"
          :label="$t('form.create')"
          :disable="!formData.name || !formData.email || !formData.block"
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
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import ProgramBlockSelect from '../../components/ProgramBlockSelect.vue';
import TrackSelect from '../../components/TrackSelect.vue';

import { iconAdd, iconEmail, iconSearch } from '@/icons';

const emit = defineEmits(['create:obj']);

const { t } = useI18n();
const store = useStore();
const { education, programs, project, projectStudents } = storeToRefs(store);

const step = ref(1);
const formData = ref({
  user: null as QuasarAutocompleteOption | null,
  track: null as number | null,
  block: null as number | null,
  name: null as string | null,
  email: null as string | null,
  number: null as string | null,
});

function userMapper(data: ApiObject[]) {
  return data.map((obj) => ({
    id: obj.id,
    name: (obj as UserTiny).name,
    caption: (obj as UserTiny).email,
    disable:
      education.value?.configuration?.allow_different_blocks_per_user_in_project === false
        ? userIdsUsedByStudents.value.has(obj.id)
        : userIdsPerBlockUsedByStudents.value.get(formData.value?.block as number) === obj.id,
  }));
}

function addStudent() {
  if (!project.value || !formData.value.user) return;

  const data = {
    user_id: formData.value.user.id,
    track: formData.value.track,
    block: formData.value.block,
    number: formData.value.number,
  };

  api.post(`${project.value.self}students/`, data).then((res) => {
    store.createObj('student', res.data);
    notify.success(t('form.student.create.success'));
    emit('create:obj');
  });
}

function createStudent() {
  api
    .get('/users/', {
      params: {
        search: formData.value.email,
      },
    })
    .then((res) => {
      if (res.data.results.length > 0) {
        formData.value.user = res.data.results[0];
        step.value = 1;
        notify.warning(t('form.student.create.exists_warning'));
        return;
      }

      const data = {
        name: formData.value.name,
        emails: [formData.value.email],
        data: {
          track_id: formData.value.track,
          block_id: formData.value.block,
          number: formData.value.number,
        },
      };

      api.post(`${project.value?.self}invite/`, data).then((res) => {
        store.createObj('student', res.data);
        notify.success(t('form.student.create.success'));
        emit('create:obj');
      });
    });
}

/**
 * Returns a map of block IDs to user IDs used by the project students.
 * @returns {Map<number, number>}
 */
const userIdsPerBlockUsedByStudents = computed<Map<number, number>>(() => {
  return projectStudents.value.reduce((map, obj) => {
    map.set(obj.block, obj.user);
    return map;
  }, new Map());
});

/**
 * Returns a set of user IDs used by the students of the current project.
 * @returns {Set<number>}
 */
const userIdsUsedByStudents = computed<Set<number>>(() => {
  return projectStudents.value.reduce((set, obj) => {
    set.add(obj.user);
    return set;
  }, new Set<number>());
});
</script>
