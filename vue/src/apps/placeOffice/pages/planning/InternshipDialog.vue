<template>
  <full-dialog icon="calendar_month" :title="internshipName">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship') }}</q-item-label>
        <q-item clickable @click="tab = 'info'" :active="tab == 'info'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="info_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Info</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'mentors'" :active="tab == 'mentors'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="people_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('mentor', 9) }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'timesheets'" :active="tab == 'timesheets'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="schedule" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('timesheet', 9) }}</q-item-section>
        </q-item>
        <q-item
          clickable
          @click="tab = 'evaluations'"
          :active="tab == 'evaluations'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon name="checklist" size="xs"></q-icon>
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
        </q-tab-panel>
        <q-tab-panel name="mentors">
          <mentors-view :editable="userIsAdmin" :obj="obj" @update:obj="(obj: Internship) => updateObj(obj)" />
        </q-tab-panel>
        <q-tab-panel name="timesheets">
          <timesheets-view :internship="obj" approvable />
        </q-tab-panel>
        <q-tab-panel name="evaluations">
          <evaluations-view :internship="obj" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer> </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import MentorsView from '@/components/stages/MentorsView.vue';
import TimesheetsView from '@/components/stages/TimesheetsView.vue';
import EvaluationsView from './EvaluationsView.vue';

const props = defineProps<{
  obj: Internship;
}>();

const store = useStore();

const { userIsAdmin } = storeToRefs(store);

const obj = ref<Internship>(props.obj);
const tab = ref<string>('info');
const internshipName = computed<string>(
  () => `${obj.value.Student?.User?.name} - ${obj.value.Place?.name} (${obj.value.Discipline?.name})`
);

function updateObj(obj: Internship) {
  store.updateObj('internship', obj);
}
</script>
