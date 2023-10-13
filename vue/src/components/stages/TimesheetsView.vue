<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md q-mt-none q-mb-none">
      {{ $t('timesheet', 9) }}
    </h4>
    <div v-if="approvable" class="col-12 col-md-2 text-right ugent__create-btn">
      <q-btn
        unelevated
        color="blue-1"
        :label="`&nbsp;${$t('form.approve')}`"
        icon="done_outline"
        class="text-ugent full-width"
        :disable="selectedPendingApproval.length === 0"
        @click="dialogVisible = true"
      />
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
    v-model:selected="selected"
  >
  </data-table>
  <q-dialog v-model="dialogVisible">
    <q-layout view="hHh lpR fFf" container class="bg-white metis__dialog-editor" style="height: 600px">
      <q-header class="bg-white q-pt-sm">
        <q-toolbar class="text-primary q-pl-lg q-pr-sm">
          <q-icon name="notes" />
          <q-toolbar-title>{{ $t('form.timesheet.approve') }}</q-toolbar-title>
          <q-space />
          <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
        </q-toolbar>
      </q-header>
      <q-page-container>
        <markdown-toast-viewer
          v-model="finalText"
          :source-text="signedText"
          class="q-px-lg"
        />
      </q-page-container>
      <q-footer class="bg-white text-dark q-pa-lg">
        <q-list class="q-my-md">
          <q-item tag="label" v-ripple>
            <q-item-section avatar top>
              <q-checkbox v-model="acceptanceChecked" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Gelezen en goedgekeurd</q-item-label>
              <q-item-label class="text-body2">
                Handtekening - door 'Gelezen en goedgekeurd' aan te vinken en op de knop 'ondertekenen' te klikken
                onderteken je dit document en erken je uitdrukkelijk dat deze dezelfde juridische waarde heeft en
                juridisch bindend is op dezelfde manier als een origineel ondertekende versie.
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <small></small>
        <div class="flex q-gutter-sm">
          <q-space />
          <q-btn
            @click="approveTimesheets"
            unelevated
            color="ugent"
            :label="$t('form.sign')"
            :disable="!acceptanceChecked"
          />
        </div>
      </q-footer>
    </q-layout>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { usePage } from '@inertiajs/vue3';

import { api } from '@/axios.ts';
import { notify } from '@/notify';

import MarkdownToastViewer from '@/components/forms/MarkdownToastViewer.vue';
import DataTable from '@/components/tables/DataTable.vue';

const props = defineProps<{
  internship: Internship;
  approvable?: boolean;
}>();

const { t } = useI18n();

const timesheets = ref<Timesheet[]>([]);
const selected = ref<Timesheet[]>([]);
const dialogVisible = ref(false);
const acceptanceChecked = ref(false);

// --
const page = usePage();
const djangoUser = computed<DjangoAuthenticatedUser>(() => page.props.django_user as DjangoAuthenticatedUser);
// --

const selectedPendingApproval = computed(() => {
  return selected.value.filter((obj) => !(obj._self as Timesheet).is_approved).sort((a, b) => (a._self as Timesheet).date.localeCompare((b._self as Timesheet).date));
});

const finalText = ref<string>('');
const signedText = computed<string>(() => {
  let text =  `Ondergetekende,

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
    sortable: true,
  },
];

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
  }));
});

function approveTimesheets() {
  if (!selected.value.length) return;

  const ids = selected.value.map((obj) => (obj._self as Timesheet).id);

  api.post(`${props.internship.rel_timesheets}approve/`, { 'ids': ids, 'signed_text': signedText.value }).then(() => {
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
