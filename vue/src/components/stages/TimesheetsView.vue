<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ $t('timesheet', 9) }}
    </h4>
  </div>
  <data-table :columns="columns" :rows="rows" sort-by="-date" hide-toolbar hide-pagination />
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';

import DataTable from '@/components/tables/DataTable.vue';

const props = defineProps<{
  internship: Internship;
  canApprove?: boolean;
}>();

const { t } = useI18n();

const timesheets = ref<Timesheet[]>([]);

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

function fetchTimesheets() {
  api.get(props.internship.rel_timesheets).then((response) => {
    timesheets.value = response.data as Timesheet[];
  });
}

onMounted(() => {
  fetchTimesheets();
});
</script>
