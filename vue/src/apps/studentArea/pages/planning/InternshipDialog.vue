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
        <q-item clickable @click="tab = 'timesheets'" :active="tab == 'timesheets'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconTimesheet" size="xs"></q-icon>
          </q-item-section>
          <q-item-section v-if="education?.configuration?.timesheets_extra_form">{{ $t('logbook') }}</q-item-section>
          <q-item-section v-else>{{ $t('timesheet', 9) }}</q-item-section>
        </q-item>
        <q-item
          clickable
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
          @click="tab = 'timesheetsForm'"
          :active="tab == 'timesheetsForm'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconTimesheetAdd" size="xs"></q-icon>
          </q-item-section>
          <q-item-section v-if="education?.configuration?.timesheets_extra_form">{{ $t('logbook') }}</q-item-section>
          <q-item-section v-else>{{ $t('timesheet', 9) }}</q-item-section>
        </q-item>
        <q-item
          v-if="obj.EvaluationForm?.has_self_evaluations"
          clickable
          @click="tab = 'evaluationsForm'"
          :active="tab == 'evaluationsForm'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon :name="iconEvaluationAdd" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('self_evaluation') }}</q-item-section>
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
                <readonly-field :label="$t('place')" :value="(obj.Place as Place).name" />
                <readonly-field
                  :label="$t('place_type')"
                  :value="((obj.Place as Place).Type as PlaceType)?.name || '-'"
                />
                <div v-if="!education?.configuration?.student_update_dates" class="row q-col-gutter-x-lg q-pl-sm">
                  <readonly-field :label="$t('field.start_date')" :value="obj.start_date" class="col-12 col-md" />
                  <readonly-field :label="$t('field.end_date')" :value="obj.end_date" class="col-12 col-md" />
                </div>
                <div v-else>
                  <div class="row q-col-gutter-x-lg">
                    <date-select
                      v-model="obj.start_date"
                      :label="$t('field.start_date')"
                      clearable
                      class="col-12 col-md"
                    />
                    <date-select v-model="obj.end_date" :label="$t('field.end_date')" clearable class="col-12 col-md" />
                  </div>
                  <q-btn @click="saveDates" outline :label="$t('form.update')" color="primary" class="q-mt-md" />
                </div>
                <div v-if="obj.Place?.phone_numbers.length" class="q-my-lg">
                  <strong>Telefonnummers</strong>
                  <q-list dense class="q-mt-sm">
                    <q-item v-for="phone in obj.Place?.phone_numbers" :key="phone.id">
                      {{ phone.number }} ({{ phone.type }})
                    </q-item>
                  </q-list>
                </div>
                <q-field
                  v-for="(address, i) in obj.Place?.addresses"
                  :key="address.id"
                  :label="`${$t('address')} #${i + 1}`"
                  readonly
                  class="col-12 col-md"
                  dense
                  stack-label
                >
                  <template #control>
                    <div class="self-center full-width no-outline" tabindex="0">
                      {{ address.address }}, {{ address.postcode }} {{ address.city }}
                    </div>
                  </template>
                  <template #append>
                    <a
                      v-if="address.mapbox_feature"
                      @click.stop
                      :href="`https://www.google.com/maps/place/${address.mapbox_feature.center[1]}+${address.mapbox_feature.center[0]}`"
                      target="_blank"
                      class="q-ml-md inherit"
                    >
                      <q-icon name="map" size="xs" />
                    </a>
                  </template>
                </q-field>
              </div>
            </div>
            <div class="col-12 col-md-6">
              <mentors-view :editable="false" :obj="obj" />
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="evaluations">
          <evaluations-view :internship="obj" show-periods />
        </q-tab-panel>
        <q-tab-panel v-if="obj.EvaluationForm?.has_self_evaluations" name="evaluationsForm">
          <evaluations-form :internship="obj" as-self-evaluation />
        </q-tab-panel>
        <q-tab-panel name="timesheets">
          <timesheets-view
            :internship="obj"
            :custom-title="education?.configuration?.timesheets_extra_form ? $t('logbook') : undefined"
          />
        </q-tab-panel>
        <q-tab-panel name="timesheetsForm">
          <div class="row q-col-gutter-sm q-mb-lg">
            <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
              <span v-if="education?.configuration?.timesheets_extra_form">{{ $t('logbook') }}</span>
              <span v-else>{{ $t('form.timesheet.title') }}</span>
            </h4>
          </div>
          <timesheets-form :internship="obj" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import DateSelect from '@/components/forms/DateSelect.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import EvaluationsForm from '@/components/stages/EvaluationsForm.vue';
import EvaluationsView from '@/components/stages/EvaluationsView.vue';
import MentorsView from '@/components/stages/MentorsView.vue';
import TimesheetsView from '@/components/stages/TimesheetsView.vue';
import TimesheetsForm from './TimesheetsForm.vue';

import { iconInfo, iconEvaluationAdd, iconEvaluations, iconInternship, iconTimesheet, iconTimesheetAdd } from '@/icons';

const props = defineProps<{
  obj: Internship;
}>();

const store = useStore();

const { education } = storeToRefs(store);

const obj = ref<Internship>(props.obj);
const tab = ref<string>('info');
const internshipName = computed<string>(
  () => `${obj.value.Student?.User?.name} - ${obj.value.Place?.name} (${obj.value.Discipline?.name})`,
);

function saveDates() {
  api
    .put(`/user/student/internships/${obj.value.id}/`, {
      start_date: obj.value.start_date,
      end_date: obj.value.end_date,
    })
    .then(() => {
      store.updateObj('internship', obj.value);
      notify.success('De stageperiode is aangepast');
    });
}
</script>
