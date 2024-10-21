<template>
  <full-dialog :icon="iconInternship" :title="internshipName">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship') }}</q-item-label>
        <q-item
          clickable
          :disable="!obj.is_approved"
          @click="tab = 'info'"
          :active="tab == 'info'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconInfo" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Info</q-item-section>
        </q-item>
        <q-item
          clickable
          :disable="!obj.is_approved"
          @click="tab = 'mentors'"
          :active="tab == 'mentors'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconMentors" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('mentor', 9) }}</q-item-section>
        </q-item>
        <q-item
          clickable
          :disable="!hasStarted || !obj.is_approved"
          @click="tab = 'timesheets'"
          :active="tab == 'timesheets'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconTimesheet" size="xs"></q-icon>
          </q-item-section>
          <q-item-section v-if="education?.configuration?.timesheets_extra_form">{{ $t('logbook') }}</q-item-section>
          <q-item-section v-else>{{ $t('timesheet', 9) }}</q-item-section>
        </q-item>
        <q-item
          clickable
          :disable="!hasStarted || !obj.is_approved"
          @click="tab = 'evaluations'"
          :active="tab == 'evaluations'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconEvaluations" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('evaluation', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('form.update') }}</q-item-label>
        <q-item
          clickable
          @click="tab = 'evaluationsForm'"
          :active="tab == 'evaluationsForm'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconEvaluationAdd" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('evaluation') }}</q-item-section>
        </q-item>
      </q-list>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-pb-lg">
        <q-tab-panel name="info">
          <div class="row q-col-gutter-xl">
            <div class="col-12 col-md-6">
              <div class="q-gutter-sm">
                <h4 class="col-12 col-md-3 q-mt-sm q-mb-none">{{ $t('internship') }}</h4>
                <readonly-field :label="$t('student')" :value="((obj.Student as Student).User as User).name" />
                <readonly-field :label="$t('field.email')" :value="((obj.Student as Student).User as User).email" />
                <div class="row q-col-gutter-x-lg q-pl-sm">
                  <readonly-field :label="$t('field.start_date')" :value="obj.start_date" class="col-12 col-md" />
                  <readonly-field :label="$t('field.end_date')" :value="obj.end_date" class="col-12 col-md" />
                </div>
              </div>
            </div>
          </div>
          <q-page-sticky v-if="!obj.is_approved" expand position="bottom" class="bg-white z-top">
            <div class="full-width full-height q-pl-md q-pr-lg q-pb-lg">
              <q-separator class="q-my-lg" />
              <div class="flex items-center">
                <q-banner v-if="userIsAdmin" rounded class="items-center bg-yellow text-ugent q-mr-xl">
                  {{ $t('form.internship.approve_msg_admin') }}
                  <q-icon name="arrow_forward" size="sm" color="ugent" class="q-ml-md" />
                </q-banner>
                <q-banner v-else rounded class="items-center bg-yellow text-ugent q-mr-xl">
                  {{ $t('form.internship.approve_msg_contact') }}
                </q-banner>
                <q-space />
                <q-btn
                  unelevated
                  color="blue-1"
                  :label="`&nbsp;${$t('form.internship.approve')}`"
                  icon="done_outline"
                  class="text-ugent"
                  :disable="sending || !userIsAdmin"
                  @click="signatureVisible = true"
                />
                <signature-dialog
                  v-model="signatureVisible"
                  :title="$t('form.internship.approve')"
                  :text-to-sign="textToSign"
                  :callback="approveInternship"
                />
              </div>
            </div>
          </q-page-sticky>
        </q-tab-panel>
        <q-tab-panel name="mentors">
          <mentors-view :editable="userIsAdmin" :obj="obj" @update:obj="(obj: Internship) => updateObj(obj)" />
        </q-tab-panel>
        <q-tab-panel name="evaluations">
          <evaluations-view :internship="obj" show-periods />
        </q-tab-panel>
        <q-tab-panel name="evaluationsForm">
          <evaluations-form :internship="obj" />
        </q-tab-panel>
        <q-tab-panel name="timesheets">
          <timesheets-view
            :internship="obj"
            :custom-title="education?.configuration?.timesheets_extra_form ? $t('logbook') : undefined"
            approvable
          />
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';

import { api } from '@/axios.ts';
import { notify } from '@/notify';
import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import SignatureDialog from '@/components/SignatureDialog.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import EvaluationsForm from '@/components/stages/EvaluationsForm.vue';
import EvaluationsView from '@/components/stages/EvaluationsView.vue';
import MentorsView from '@/components/stages/MentorsView.vue';
import TimesheetsView from '@/components/stages/TimesheetsView.vue';

import { iconEvaluationAdd, iconEvaluations, iconInfo, iconInternship, iconMentors, iconTimesheet } from '@/icons';

const { t } = useI18n();

const props = defineProps<{
  obj: Internship;
}>();

const store = useStore();

const { education, userIsAdmin } = storeToRefs(store);

const obj = ref<Internship>(props.obj);
const tab = ref<string>('info');
const internshipName = computed<string>(
  () => `${obj.value.Student?.User?.name} - ${obj.value.Place?.name} (${obj.value.Discipline?.name})`,
);
const hasStarted = computed<boolean>(() => {
  if (!obj.value.start_date) return false;
  return new Date(obj.value.start_date) <= new Date();
});

const sending = ref<boolean>(false);
const signatureVisible = ref<boolean>(false);

const textToSign = computed<string>(() => {
  /* TODO: this should come from the backend */
  if (education.value?.code == 'gezveb') {
    return `Als u na het kennismakingsgesprek met de student besloten heeft om de student te ontvangen voor stage dit academiejaar (periode april – juni) vragen we om u akkoord te verklaren met de stage door hieronder 'Gelezen en goedgekeurd' aan te vinken.`;
  }

  return `Stageplaats ${obj.value.Place?.name} is bereid om student ${obj.value.Student?.User?.name} van de UGent (studentennummer ${obj.value.Student?.number}) te begeleiden tijdens de stage ${education.value?.short_name} van ${obj.value.start_date} tot ${obj.value.start_date}.`;
});

function updateObj(obj: Internship) {
  store.updateObj('internship', obj);
}

function approveInternship() {
  sending.value = true;

  if (obj.value.is_approved) {
    return;
  }

  api
    .post(`${obj.value.self}approve/`, { signed_text: textToSign.value })
    .then(() => {
      notify.success(t('form.internship.approved'));
      obj.value.is_approved = true;
      updateObj(obj.value);
    })
    .finally(() => {
      sending.value = false;
    });
}
</script>
