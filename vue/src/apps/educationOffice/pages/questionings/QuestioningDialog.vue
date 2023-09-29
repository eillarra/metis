<template>
  <full-dialog icon="task_alt" :title="$t('questioning')">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('progress') }}</q-item-label>
        <q-item clickable @click="tab = 'responses'" :active="tab == 'responses'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="list_alt" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('response', 9) }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'pending'" :active="tab == 'pending'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="error_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('pending') }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('configuration') }}</q-item-label>
        <q-item clickable @click="tab = 'email'" :active="tab == 'email'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="mail_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('email_template') }}</q-item-section>
        </q-item>
        <!--<q-item clickable @click="tab = 'form'" :active="tab == 'form'"  active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="checklist" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('form_builder') }}</q-item-section>
        </q-item>-->
      </q-list>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-pb-lg">
        <q-tab-panel name="responses">
          <div class="row q-col-gutter-sm q-mb-lg">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
              {{ $t('response', 9) }} ({{ responses.length }}/{{ targetObjectsLength }})
            </h4>
          </div>
          <responded-project-places-table v-if="props.obj.type.startsWith('project_place_')" :responses="responses" />
          <responded-students-table v-if="props.obj.type.startsWith('student_')" :responses="responses" />
        </q-tab-panel>
        <q-tab-panel name="pending">
          <div class="row q-col-gutter-sm q-mb-lg">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
              {{ $t('pending', 9) }} ({{ objectsPendingResponse.length }}/{{ targetObjectsLength }})
            </h4>
          </div>
          <pending-project-places-table
            v-if="props.obj.type.startsWith('project_place_')"
            :questioning="props.obj"
            :project-places="(objectsPendingResponse as ProjectPlace[])"
          />
          <pending-students-table
            v-if="props.obj.type.startsWith('student_')"
            :questioning="props.obj"
            :students="(objectsPendingResponse as Student[])"
          />
        </q-tab-panel>
        <q-tab-panel name="email">
          <div class="row q-col-gutter-sm q-mb-sm">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">{{ $t('email_template') }}</h4>
          </div>
          <q-input v-model="obj.email_subject" :label="$t('field.subject')" class="q-mb-md" />
          <markdown-toast-editor v-model="obj.email_body" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <q-separator />
      <div v-if="tab == 'email'" class="flex q-gutter-sm q-pa-lg">
        <q-space />
        <q-btn @click="saveEmail" unelevated color="ugent" :label="$t('form.save')" />
      </div>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { notify } from '@/notify';
import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import MarkdownToastEditor from '@/components/forms/MarkdownToastEditor.vue';
import PendingProjectPlacesTable from './sections/PendingProjectPlacesTable.vue';
import PendingStudentsTable from './sections/PendingStudentsTable.vue';
import RespondedProjectPlacesTable from './sections/RespondedProjectPlacesTable.vue';
import RespondedStudentsTable from './sections/RespondedStudentsTable.vue';

const props = defineProps<{
  obj: Questioning;
}>();

const { t } = useI18n();
const store = useStore();
const { projectPlaces, projectStudents } = storeToRefs(store);

const responses = ref<CustomFormResponse[]>([]);
const tab = ref('responses');
const obj = ref<Questioning>(props.obj);

const responseObjectIds = computed<Set<number>>(() => new Set(responses.value.map((response) => response.object_id)));
const targetObjects = computed(() => {
  if (!props.obj) return [];
  if (props.obj.type.startsWith('student_')) {
    return projectStudents.value.filter((student) => props.obj.target_object_ids?.includes(student.id)) as Student[];
  }
  if (props.obj.type.startsWith('project_place_')) {
    return projectPlaces.value.filter((place) => props.obj.target_object_ids?.includes(place.id)) as ProjectPlace[];
  }
  return [];
});
const targetObjectsLength = computed(() => props.obj.target_object_ids?.length);

const objectsPendingResponse = computed(() => {
  return targetObjects.value.filter((object) => !responseObjectIds.value.has(object.id));
});

function saveEmail() {
  api
    .patch(obj.value.self, {
      email_subject: obj.value.email_subject,
      email_body: obj.value.email_body,
    })
    .then(() => {
      notify.success(t('form.questioning.saved'));
      store.updateObj('questioning', obj.value);
    });
}

async function fetchResponses() {
  const { data } = await api.get<CustomFormResponse[]>(props.obj.rel_responses);
  responses.value = data.map((response) => {
    return {
      ...response,
      _object: targetObjects.value.find((object) => object.id === response.object_id),
    };
  });
}

fetchResponses();

watch(
  () => props.obj,
  () => {
    tab.value = 'responses';
  }
);
</script>
