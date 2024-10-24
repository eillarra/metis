<template>
  <full-dialog :icon="iconInternship" :title="internshipName">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship') }}</q-item-label>
        <q-item clickable @click="tab = 'info'" :active="tab == 'info'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconInfo" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Info</q-item-section>
        </q-item>
        <q-item
          clickable
          :disable="!obj.Place"
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
          :disable="!hasStarted"
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
          :disable="!hasStarted"
          @click="tab = 'evaluations'"
          :active="tab == 'evaluations'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconEvaluations" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('evaluation', 9) }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'documents'" :active="tab == 'documents'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconFiles" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('other') }}</q-item-label>
        <q-item clickable @click="tab = 'actions'" :active="tab == 'actions'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconActions" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('action', 9) }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'remarks'" :active="tab == 'remarks'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="hasRemarks ? iconChatBadge : iconChat" size="xs" />
          </q-item-section>
          <q-item-section>{{ $t('remark', 9) }}</q-item-section>
        </q-item>
        <q-item :disabled="true" :active="tab == 'program'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconProgram" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('program') }}</q-item-section>
        </q-item>
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
        <q-tab-panel name="info">
          <div class="row q-col-gutter-xl">
            <div class="col-12 col-md-8">
              <div class="q-gutter-sm">
                <readonly-field :label="$t('project')" :value="projectName" />
                <readonly-field :label="$t('student')" :value="obj.Student?.User?.name || '-'" />
                <period-select v-model="obj.period" :periods="filteredPeriods" :label="$t('period')" />
                <discipline-select
                  v-if="education"
                  v-model="obj.discipline"
                  :disciplines="education.disciplines"
                  :label="$t('discipline')"
                />
                <div class="row q-col-gutter-lg q-pt-sm q-pl-sm">
                  <date-select
                    v-model="obj.start_date"
                    :label="$t('field.start_date')"
                    clearable
                    class="col-12 col-md"
                  />
                  <date-select v-model="obj.end_date" :label="$t('field.end_date')" clearable class="col-12 col-md" />
                </div>
              </div>
            </div>
            <div class="col-12 col-md">
              <place-box :place="obj.Place as Place"></place-box>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="mentors">
          <mentors-view editable :obj="obj" @update:obj="(obj: Internship) => updateObj(obj)" />
        </q-tab-panel>
        <q-tab-panel name="timesheets">
          <timesheets-view
            :internship="obj"
            :custom-title="education?.configuration?.timesheets_extra_form ? $t('logbook') : undefined"
          />
        </q-tab-panel>
        <q-tab-panel name="evaluations">
          <evaluations-view :internship="obj" show-points />
        </q-tab-panel>
        <q-tab-panel name="documents">
          <files-view :api-endpoint="obj.rel_files" :visibility-options="['place', 'student']" />
        </q-tab-panel>
        <q-tab-panel name="actions">
          <internship-actions :internship="obj" />
        </q-tab-panel>
        <q-tab-panel name="emails">
          <div class="row q-col-gutter-lg q-mb-none">
            <h4 class="col-12 col-md-6 q-mt-none q-mb-lg">
              {{ $t('field.email', 9) }}
            </h4>
          </div>
          <emails-view :emails="emails" :tags="[`internship.id:${obj.id}`]" />
        </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoint="obj.rel_remarks" />
        </q-tab-panel>
        <q-tab-panel name="updated_by">
          <updated-by-view :obj="obj" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <div v-if="tab == 'info'" class="flex q-gutter-sm q-pa-lg">
        <q-space />
        <q-btn @click="save" unelevated color="ugent" :label="$t('form.internship.save')" />
      </div>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import PlaceBox from '@/components/PlaceBox.vue';
import EmailsView from '@/components/emails/EmailsView.vue';
import DateSelect from '@/components/forms/DateSelect.vue';
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import UpdatedByView from '@/components/forms/UpdatedByView.vue';
import FilesView from '@/components/rel/FilesView.vue';
import RemarksView from '@/components/rel/RemarksView.vue';
import EvaluationsView from '@/components/stages/EvaluationsView.vue';
import MentorsView from '@/components/stages/MentorsView.vue';
import TimesheetsView from '@/components/stages/TimesheetsView.vue';
import PeriodSelect from '../../components/PeriodSelect.vue';
import InternshipActions from './InternshipActions.vue';

import {
  iconActions,
  iconChat,
  iconChatBadge,
  iconEmails,
  iconEvaluations,
  iconFiles,
  iconInfo,
  iconInternship,
  iconMentors,
  iconProgram,
  iconTimesheet,
} from '@/icons';

defineEmits(['delete:obj']);

const props = defineProps<{
  obj: Internship;
}>();

const { t } = useI18n();
const store = useStore();
const { education, project, emails } = storeToRefs(store);

const obj = ref<Internship>(props.obj);
const tab = ref<string>('info');
const projectName = computed<string>(() => (project.value ? project.value.name : ''));
const internshipName = computed<string>(
  () => `${obj.value.Student?.User?.name} - ${obj.value.Place?.name || ''} (${obj.value.Discipline?.name})`,
);
const hasStarted = computed<boolean>(() => {
  if (!obj.value.start_date) return false;
  return new Date(obj.value.start_date) <= new Date();
});

const hasRemarks = computed<boolean>(() => (Number(obj.value._tags_dict?.['remarks.count']) || 0) > 0);

const filteredPeriods = computed(() => {
  if (!project.value) return [];
  if (!obj.value.Student?.Track) return (project.value as Project).periods;

  return (project.value as Project).periods.filter((period) => {
    return (
      obj.value.Student?.block == period.ProgramInternship?.block &&
      obj.value.Student?.Track?.program_internships.includes(period.program_internship)
    );
  });
});

function save() {
  api
    .put(obj.value.self, {
      ...obj.value,
      student: obj.value.Student?.id,
      track: obj.value.Track?.id,
    })
    .then((res) => {
      obj.value.updated_at = res.data.updated_at;
      obj.value.updated_by = res.data.updated_by;
      store.updateObj('projectInternship', obj.value);
      notify.success(t('form.internship.saved'));
    });
}

function updateObj(obj: Internship) {
  store.updateObj('projectInternship', obj);
}
</script>
