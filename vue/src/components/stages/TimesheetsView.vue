<template>
  <div class="row q-col-gutter-sm q-mb-none">
    <h4 class="col-12 col-md-6 q-mt-none q-mb-lg use-default-q-btn">
      <span v-if="customTitle">{{ customTitle }}</span>
      <span v-else>{{ $t('timesheet', 9) }}</span>
      <!--<a v-show="timesheets.length" href="#" target="_blank">
        <q-btn round outline :icon="iconDownload" size="sm" color="primary" class="q-ml-md q-pa-xs">
          <q-tooltip :delay="250">{{ $t('download.pdf') }}</q-tooltip>
        </q-btn>
      </a>-->
    </h4>
    <div v-if="approvable" class="col-12 col-md text-right q-gutter-sm">
      <q-btn
        unelevated
        color="blue-1"
        :label="`&nbsp;${$t('form.select_all_pending')}`"
        icon="check_box"
        class="text-ugent"
        :disable="totalPendingApproval == '-'"
        @click="selectPending"
      />
      <q-btn
        unelevated
        color="blue-1"
        :label="`&nbsp;${$t('form.approve')}`"
        icon="done_outline"
        class="text-ugent"
        :disable="selected.length === 0"
        @click="dialogVisible = true"
      />
    </div>
  </div>
  <div class="row q-col-gutter-md q-mb-lg">
    <div class="col-12 col-md-3">
      <q-card flat class="bg-grey-2 q-pa-md metis__dashcard">
        <span class="text-h5 text-ugent float-right">{{ totalTime }}</span>
        <small>{{ $t('form.timesheet.help.time_total') }}</small>
      </q-card>
    </div>
    <div class="col-12 col-md-3">
      <q-card flat class="bg-grey-2 q-pa-md metis__dashcard">
        <span class="text-h5 text-grey-8 float-right">{{ totalPendingApproval }}</span>
        <small>{{ $t('form.timesheet.help.time_pending') }}</small>
      </q-card>
    </div>
  </div>
  <data-table
    :columns="columns"
    :rows="rows"
    sort-by="-date"
    :rows-per-page="10"
    hide-toolbar
    in-dialog
    :selection="approvable ? 'multiple' : 'none'"
    :form-component="withComments ? TimesheetDialog : undefined"
    open-dialog
    v-model:selected="selected"
  >
  </data-table>
  <signature-dialog
    v-model="dialogVisible"
    :title="$t('form.timesheet.approve')"
    :text-to-sign="textToSign"
    :callback="approveTimesheets"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { usePage } from '@inertiajs/vue3';

import { api } from '@/axios.ts';
import { notify } from '@/notify';
import { sumHours } from '@/utils/dates';

import TimesheetDialog from './TimesheetDialog.vue';
import SignatureDialog from '@/components/SignatureDialog.vue';
import DataTable from '@/components/tables/DataTable.vue';

const props = defineProps<{
  internship: Internship;
  approvable?: boolean;
  customTitle?: string | undefined;
}>();

const { t } = useI18n();

// --
const page = usePage();
const education = computed<Education>(() => page.props.education as Education);
const djangoUser = computed<DjangoAuthenticatedUser>(() => page.props.django_user as DjangoAuthenticatedUser);
// --

const timesheets = ref<Timesheet[]>([]);
const selected = ref<QuasarTableRow[]>([]);
const dialogVisible = ref(false);
const acceptanceChecked = ref(false);

const withComments = computed(() => education.value.configuration?.timesheets_extra_form);

const selectedPendingApproval = computed(() => {
  return selected.value
    .filter((obj) => !(obj._self as Timesheet).is_approved)
    .sort((a, b) => (a._self as Timesheet).date.localeCompare((b._self as Timesheet).date));
});

const textToSign = computed<string>(() => {
  let text = `Ondergetekende,

${djangoUser.value.first_name} ${djangoUser.value.last_name} (${djangoUser.value.email}) medewerker op stageplaats ${props.internship.Place?.name} bevestigt dat student ${props.internship.Student?.User?.name} met studentennummer ${props.internship.Student?.number} hier stage heeft gelopen op:
`;

  for (const timesheet of selectedPendingApproval.value) {
    const times = [];
    if (timesheet.start_time_am != '-') times.push(`van ${timesheet.start_time_am} tot ${timesheet.end_time_am}`);
    if (timesheet.start_time_pm != '-') times.push(`van ${timesheet.start_time_pm} tot ${timesheet.end_time_pm}`);
    text += `\n- ${timesheet.date}, ${times.join(' en ')} (duur: ${timesheet.duration})`;
  }

  return text;
});

const totalTime = computed<string>(() => {
  if (!timesheets.value.length) return '-';
  const total = sumHours(timesheets.value.map((obj) => obj.duration));
  return (total != '0:00' ? total : '-') as string;
});

const totalPendingApproval = computed<string>(() => {
  if (!timesheets.value.length) return '-';
  const total = sumHours(timesheets.value.filter((obj) => !obj.is_approved).map((obj) => obj.duration));
  return (total != '0:00' ? total : '-') as string;
});

const columns = [
  {
    name: 'date',
    field: 'date',
    required: true,
    label: t('field.date'),
    align: 'left',
    sortable: true,
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'start_time_am',
    field: 'start_time_am',
    label: `${t('field.start_time')} (am)`,
    align: 'left',
  },
  {
    name: 'end_time_am',
    field: 'end_time_am',
    label: `${t('field.end_time')} (am)`,
    align: 'left',
  },
  {
    name: 'start_time_pm',
    field: 'start_time_pm',
    label: `${t('field.start_time')} (pm)`,
    align: 'left',
  },
  {
    name: 'end_time_pm',
    field: 'end_time_pm',
    label: `${t('field.end_time')} (pm)`,
    align: 'left',
  },
  {
    name: 'duration',
    field: 'duration',
    label: t('field.duration'),
    align: 'left',
  },
  {
    name: 'is_approved',
    field: 'is_approved',
    label: t('field.approved'),
    align: 'center',
  },
];

if (withComments.value) {
  columns.push({
    name: 'has_extra_data',
    field: 'has_extra_data',
    label: t('form.timesheet.comments'),
    align: 'center',
  });
}

const rows = computed(() => {
  return timesheets.value.map((obj: Timesheet) => ({
    _hide_selection: obj.is_approved || new Date() < new Date(`${obj.date} ${obj.end_time_pm || obj.end_time_am}`),
    _self: obj,
    date: obj.date,
    start_time_am: obj.start_time_am ? obj.start_time_am.substring(0, 5) : '-',
    end_time_am: obj.end_time_am ? obj.end_time_am.substring(0, 5) : '-',
    start_time_pm: obj.start_time_pm ? obj.start_time_pm.substring(0, 5) : '-',
    end_time_pm: obj.end_time_pm ? obj.end_time_pm.substring(0, 5) : '-',
    duration: obj.duration.substring(0, 5),
    is_approved: obj.is_approved,
    has_extra_data: Object.keys(obj.data).length > 0,
  }));
});

function selectPending() {
  selected.value = [...rows.value.filter((obj) => !(obj._self as Timesheet).is_approved)];
}

function approveTimesheets() {
  if (!selected.value.length) return;

  const ids = selected.value.map((obj) => (obj._self as Timesheet).id);

  api.post(`${props.internship.rel_timesheets}approve/`, { ids: ids, signed_text: textToSign.value }).then(() => {
    notify.success(t('form.timesheet.approved'));
    fetchTimesheets();
    reset();
  });
}

function reset() {
  dialogVisible.value = false;
  acceptanceChecked.value = false;
  selected.value = [];
}

function fetchTimesheets() {
  api.get(props.internship.rel_timesheets).then((response) => {
    timesheets.value = response.data as Timesheet[];
  });
}

onMounted(() => {
  fetchTimesheets();
});
</script>
