<template>
  <div class="row q-col-gutter-xl">
    <div class="col-12 col-md-4">
      <q-date
        v-model="date"
        mask="YYYY-MM-DD"
        :navigation-min-year-month="yearMonths.min"
        :navigation-max-year-month="yearMonths.max"
        :default-year-month="yearMonths.default"
        :options="availableDates"
        :events="markedDates"
        :event-color="dateColors"
        minimal
        flat
        bordered
      />
    </div>
    <div class="col-12 col-md-4">
      <div v-if="!date">
        <h5 class="text-body1 text-strong q-mt-none">{{ $t('form.timesheet.help.choose_date') }}</h5>
        <p>{{ $t('form.timesheet.help.calendar_colors') }}</p>
      </div>
      <div v-else class="q-gutter-sm">
        <h5 v-if="!obj.self" class="text-body1 text-strong">{{ $t('form.timesheet.create.new') }}</h5>
        <h5 v-else class="text-body1 text-strong">{{ $t('form.timesheet.edit') }}</h5>
        <readonly-field :label="$t('field.date')" :value="date">
          <template #append>
            <q-badge v-if="obj.is_approved" color="green" text-color="white" :label="$t('field.approved')" />
          </template>
        </readonly-field>
        <div class="row q-col-gutter-lg q-pt-sm q-pl-sm">
          <date-select
            type="time"
            v-model="obj.start_time_am"
            :readonly="obj.is_approved"
            :label="`${$t('field.start_time')} (am)`"
            clearable
            class="col-12 col-md"
            :options="(hr, min) => limitTimeOptions(hr, min)"
          />
          <date-select
            type="time"
            v-model="obj.end_time_am"
            :readonly="obj.is_approved"
            :disable="!obj.is_approved && !obj.start_time_am"
            :label="`${$t('field.end_time')} (am)`"
            clearable
            class="col-12 col-md"
            :options="(hr, min) => limitTimeOptions(hr, min, obj.start_time_am)"
          />
        </div>
        <div class="row q-col-gutter-lg q-pt-sm q-pl-sm">
          <date-select
            type="time"
            v-model="obj.start_time_pm"
            :readonly="obj.is_approved"
            :label="`${$t('field.start_time')} (pm)`"
            clearable
            class="col-12 col-md"
            :options="(hr, min) => limitTimeOptions(hr, min, obj.end_time_am)"
          />
          <date-select
            type="time"
            v-model="obj.end_time_pm"
            :readonly="obj.is_approved"
            :disable="!obj.is_approved && !obj.start_time_pm"
            :label="`${$t('field.end_time')} (pm)`"
            clearable
            class="col-12 col-md"
            :options="(hr, min) => limitTimeOptions(hr, min, obj.start_time_pm)"
          />
        </div>
        <q-input
          v-show="education?.configuration?.timesheets_with_comments"
          v-model="obj.comments"
          :label="$t('form.timesheet.comments')"
          :readonly="obj.is_approved"
          :disable="obj.is_approved"
          type="textarea"
          class="q-mt-md"
        />
        <q-btn
          unelevated
          @click="createOrUpdateTimesheet"
          color="ugent"
          :label="obj.self ? $t('form.update') : $t('form.create')"
          :disable="
            Boolean(
              obj.is_approved ||
                !date ||
                (!obj.start_time_am && !obj.start_time_pm) ||
                (obj.start_time_am && !obj.end_time_am) ||
                (obj.start_time_pm && !obj.end_time_pm)
            )
          "
          class="q-mt-lg"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { useStore } from '../../store.js';

import { api } from '@/axios';
import { notify } from '@/notify';
import { formatDate } from '@/utils/dates';

import DateSelect from '@/components/forms/DateSelect.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';

const props = defineProps<{
  internship: Internship;
}>();

const { education } = storeToRefs(useStore());
const { t } = useI18n();

const timesheets = ref<Timesheet[]>([]);
const date = ref(null);
const obj = ref({
  self: null as number | null,
  start_time_am: null as string | null,
  end_time_am: null as string | null,
  start_time_pm: null as string | null,
  end_time_pm: null as string | null,
  is_approved: false,
  comments: '',
});

const timesheetsByDate = computed<Record<string, Timesheet>>(() => {
  return timesheets.value.reduce((acc, timesheet) => {
    acc[formatDate(timesheet.date, 'YYYY/MM/DD')] = timesheet;
    return acc;
  }, {} as Record<string, Timesheet>);
});

const yearMonths = computed<{
  min: string;
  max: string;
  default: string;
}>(() => ({
  min: formatDate(props.internship.start_date, 'YYYY/MM'),
  max: formatDate(props.internship.end_date, 'YYYY/MM'),
  default: formatDate(new Date().toDateString(), 'YYYY/MM'),
}));

function availableDates(date: string) {
  return (
    date >= formatDate(props.internship.start_date, 'YYYY/MM/DD') &&
    date <= formatDate(props.internship.end_date, 'YYYY/MM/DD') &&
    date <= formatDate(new Date().toDateString(), 'YYYY/MM/DD')
  );
}

const markedDates = computed<string[]>(() => {
  return timesheets.value.map((timesheet) => formatDate(timesheet.date, 'YYYY/MM/DD'));
});

function dateColors(date: string) {
  if (date in timesheetsByDate.value) {
    return timesheetsByDate.value[date].is_approved ? 'green' : 'orange';
  }

  return 'grey';
}

function fetchTimesheets() {
  api.get(props.internship.rel_timesheets).then((response) => {
    timesheets.value = response.data;
  });
}

function createTimesheet() {
  api
    .post(props.internship.rel_timesheets, {
      date: date.value,
      start_time_am: obj.value.start_time_am,
      end_time_am: obj.value.end_time_am,
      start_time_pm: obj.value.start_time_pm,
      end_time_pm: obj.value.end_time_pm,
      comments: obj.value.comments,
    })
    .then((response) => {
      timesheets.value.push(response.data);
      obj.value = response.data;
      notify.success(t('form.timesheet.create.success'));
    });
}

function updateTimesheet() {
  api
    .put(obj.value.self, {
      date: obj.value.date,
      start_time_am: obj.value.start_time_am,
      end_time_am: obj.value.end_time_am,
      start_time_pm: obj.value.start_time_pm,
      end_time_pm: obj.value.end_time_pm,
      comments: obj.value.comments,
    })
    .then((response) => {
      const index = timesheets.value.findIndex((timesheet) => timesheet.id == obj.value.id);
      timesheets.value[index] = response.data;
      notify.success(t('form.timesheet.saved'));
    });
}

function createOrUpdateTimesheet() {
  if (obj.value.self) updateTimesheet();
  else createTimesheet();
}

onMounted(() => {
  fetchTimesheets();
});

watch(date, () => {
  const formattedDate = formatDate(date.value, 'YYYY/MM/DD');

  if (formattedDate in timesheetsByDate.value) {
    obj.value = timesheetsByDate.value[formattedDate];
  } else {
    obj.value = {
      self: null,
      start_time_am: null,
      end_time_am: null,
      start_time_pm: null,
      end_time_pm: null,
    };
  }
});

function limitTimeOptions(hr: number, min: number, pastTime?: string | null) {
  if (min % 5 !== 0) return false;
  if (!pastTime) return true;

  const splits = pastTime.split(':');
  if (hr < +splits[0]) return false;
  if (hr !== null && min !== null && hr === +splits[0] && min <= +splits[1]) return false;
  return true;
}
</script>
