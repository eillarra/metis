<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="InternshipDialog"
    :create-form-component="InternshipCreateForm"
    sort-by="start_date"
    open-dialog
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import InternshipCreateForm from './InternshipCreateForm.vue';
import InternshipDialog from './InternshipDialog.vue';

const { t } = useI18n();

const props = defineProps<{
  internships: Internship[];
}>();

const queryColumns = ['student_name', 'student_number', 'place_name'];

const columns = [
  {
    name: 'student_name',
    field: 'student_name',
    required: true,
    label: t('student'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'place_name',
    field: 'place_name',
    required: true,
    label: t('place'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
  },
  {
    name: 'track_name',
    field: 'track_name',
    label: t('track'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'block_name',
    field: 'block_name',
    label: t('program_block'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'period_name',
    field: 'period_name',
    label: t('period'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'check_hours',
    field: 'check_hours',
    label: t('hour', 9),
    align: 'right',
    autoWidth: true,
    classes: 'panno-mono-number',
    sortable: true,
    sort: (a: [number, boolean], b: [number, boolean]) => a[0] - b[0],
  },
  {
    name: 'steps',
    field: 'evaluation_steps',
    label: t('evaluation', 9),
    align: 'left',
  },
  {
    name: 'disciplines',
    field: 'disciplines',
    label: t('discipline'),
    align: 'left',
  },
  {
    name: 'status',
    field: 'status',
    label: t('field.status'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'start_date',
    field: 'start_date',
    label: t('field.start_date'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'end_date',
    field: 'end_date',
    label: t('field.end_date'),
    align: 'left',
    sortable: true,
    autoWidth: true,
  },
  {
    name: 'has_mentors',
    field: 'has_mentors',
    label: t('mentor', 9),
    align: 'center',
  },
  {
    name: 'is_approved',
    field: 'is_approved',
    label: t('field.approved'),
    align: 'center',
  },
];

const statusLabels = {
  preplanning: t('internship_status.preplanning'),
  concept: t('internship_status.concept'),
  definitive: t('internship_status.definitive'),
  cancelled: t('internship_status.cancelled'),
  unsuccessful: t('internship_status.unsuccessful'),
};

const rows = computed(() => {
  return props.internships.map((obj: Internship) => ({
    _self: obj,
    _class:
      obj.status === 'cancelled'
        ? 'bg-red-1'
        : obj.status === 'unsuccessful'
        ? 'bg-orange-1'
        : !obj.is_approved
        ? 'bg-yellow-1'
        : '',
    student_name: (obj.Student?.User as StudentUser)?.name || '-',
    student_number: obj.Student?.number || '-',
    place_name: obj.Place?.name || '-',
    block_name: obj.Period?.ProgramInternship?.Block?.name || '-',
    period_name: obj.Period?.ProgramInternship ? `P${obj.Period.ProgramInternship.position}` : '-',
    track_name: obj.Track?.name || '-',
    check_hours: [
      Number(obj.tag_objects?.['hours.total']?.split(':')[0]) || 0,
      (obj.tag_objects?.['hours.total'] || '-') == (obj.tag_objects?.['hours.approved'] || '-'),
    ],
    evaluation_steps: obj.status === 'definitive' && obj.is_approved ? getEvaluationSteps(obj) : [],
    disciplines: obj.Discipline ? [obj.Discipline] : [],
    status: statusLabels[obj.status as keyof typeof statuses] || obj.status,
    start_date: obj.start_date,
    end_date: obj.end_date,
    has_mentors: obj.mentors.filter((mentor: Mentor) => mentor.user.last_login).length > 0,
    is_approved: obj.is_approved,
  }));
});

function getEvaluationSteps(internship: Internship) {
  const evaluationSteps = [];

  for (const tag of internship.tags) {
    if (tag.startsWith('intermediate.')) {
      const [number, status] = tag.substring(13).split(':');
      let color = '';

      if (status === 'approved') {
        color = 'dark';
      } else if (status === 'not_approved') {
        color = 'orange-8';
      } else if (status === 'pending') {
        color = 'grey-4';
      }

      // add the icon and color to the array
      evaluationSteps.push({
        number: number,
        icon: number == '0' ? 'library_add_check' : `filter_${number}`,
        color: color,
      });
    }
  }

  evaluationSteps.sort((a, b) => {
    if (a.number === '0') {
      return 1;
    }
    if (b.number === '0') {
      return -1;
    }
    return parseInt(a.number) - parseInt(b.number);
  });

  return evaluationSteps;
}
</script>
