<template>
  <full-dialog :icon="iconQuestioning" :title="$t('questioning')">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('progress') }}</q-item-label>
        <q-item clickable @click="tab = 'responses'" :active="tab == 'responses'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconResponses" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('response', 9) }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'pending'" :active="tab == 'pending'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconResponsesPending" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('pending') }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'documents'" :active="tab == 'documents'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconFiles" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item
          v-if="obj.type == 'student_tops'"
          clickable
          @click="tab = 'planner'"
          :active="tab == 'planner'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconRobot" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('planner') }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('configuration') }}</q-item-label>
        <q-item clickable @click="tab = 'email'" :active="tab == 'email'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconEmailSettings" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('email_template') }}</q-item-section>
          <q-item-section v-if="!hasEmail" side style="padding-left: 0">
            <q-icon :name="iconTableCheckPending" color="orange" size="12px" />
          </q-item-section>
        </q-item>
        <!--<q-item clickable @click="tab = 'form'" :active="tab == 'form'"  active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="checklist" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('form_builder') }}</q-item-section>
        </q-item>-->
        <q-item-label header>Logs</q-item-label>
        <q-item clickable @click="tab = 'emails'" :active="tab == 'emails'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconEmails" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('field.email', 9) }}</q-item-section>
        </q-item>
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
            :project-places="objectsPendingResponse as ProjectPlace[]"
            :show-actions="hasEmail"
          />
          <pending-students-table
            v-if="props.obj.type.startsWith('student_')"
            :questioning="props.obj"
            :students="objectsPendingResponse as Student[]"
            :show-actions="hasEmail"
          />
        </q-tab-panel>
        <q-tab-panel name="documents">
          <div class="row q-col-gutter-sm q-mb-sm">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">{{ $t('document', 9) }}</h4>
          </div>
          <ul>
            <li><a :href="`/nl/files/q/${obj.id}.pdf`" target="_blank">Antwoorden (PDF)</a></li>
            <li><a :href="`/nl/files/q/${obj.id}.xlsx`" target="_blank">Antwoorden (Excel)</a></li>
          </ul>
        </q-tab-panel>
        <q-tab-panel name="planner">
          <div class="row q-col-gutter-sm q-mb-sm">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">{{ $t('planner') }}</h4>
          </div>
          <planner-view :questioning="obj" :students="targetObjects as Student[]" :project-places="projectPlaces" />
        </q-tab-panel>
        <q-tab-panel name="email">
          <div class="row q-col-gutter-sm">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">{{ $t('email_template') }}</h4>
            <div class="col-12 col-md text-right ugent__create-btn">
              <q-btn
                unelevated
                :color="obj.disable_automatic_emails ? 'red-1' : 'blue-1'"
                :class="obj.disable_automatic_emails ? 'text-red' : 'text-ugent'"
              >
                <q-toggle
                  v-model="obj.disable_automatic_emails"
                  :label="
                    obj.disable_automatic_emails
                      ? `&nbsp;${$t('form.questioning.automatic_emails_disabled')}`
                      : `&nbsp;${$t('form.questioning.automatic_emails_enabled')}`
                  "
                  :true-value="false"
                  :false-value="true"
                  class="q-pr-md"
                />
              </q-btn>
            </div>
          </div>
          <q-input v-model="obj.email_subject" :label="$t('field.subject')" class="q-mb-md" />
          <markdown-toast-editor v-model="obj.email_body" />
        </q-tab-panel>
        <q-tab-panel name="emails">
          <div class="row q-col-gutter-lg q-mb-none">
            <h4 class="col-12 col-md-6 q-mt-none q-mb-lg">
              {{ $t('field.email', 9) }}
            </h4>
          </div>
          <emails-view :emails="emails" :tags="[`questioning.id:${obj.id}`]" in-dialog />
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
import EmailsView from '@/components/emails/EmailsView.vue';
import MarkdownToastEditor from '@/components/forms/MarkdownToastEditor.vue';
import PendingProjectPlacesTable from './sections/PendingProjectPlacesTable.vue';
import PendingStudentsTable from './sections/PendingStudentsTable.vue';
import PlannerView from './sections/PlannerView.vue';
import RespondedProjectPlacesTable from './sections/RespondedProjectPlacesTable.vue';
import RespondedStudentsTable from './sections/RespondedStudentsTable.vue';

import {
  iconEmails,
  iconEmailSettings,
  iconFiles,
  iconResponsesPending,
  iconQuestioning,
  iconResponses,
  iconRobot,
  iconTableCheckPending,
} from '@/icons';

const props = defineProps<{
  obj: Questioning;
}>();

const { t } = useI18n();
const store = useStore();
const { emails, projectPlaces, projectStudents } = storeToRefs(store);

const responses = ref<CustomFormResponse[]>([]);
const tab = ref('responses');
const obj = ref<Questioning>(props.obj);

const hasEmail = computed(() => !!obj.value.email_subject && !!obj.value.email_body);
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
  },
);
</script>
