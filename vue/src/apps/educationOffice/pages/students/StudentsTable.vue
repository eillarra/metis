<template>
  <data-table
    :columns="columns"
    :rows="rows"
    :query-columns="queryColumns"
    :form-component="StudentForm"
    :create-form-component="StudentCreateForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { formatDate } from '@/utils/dates';

import { useStore } from '../../store.js';

import DataTable from '@/components/tables/DataTable.vue';
import StudentCreateForm from './StudentCreateForm.vue';
import StudentForm from './StudentForm.vue';

const { t } = useI18n();
const { project } = storeToRefs(useStore());

const props = defineProps<{
  students: StudentUser[];
}>();

const queryColumns = ['name', 'email', 'number'];

const columns = [
  {
    name: 'name',
    field: 'name',
    required: true,
    label: t('field.name'),
    align: 'left',
    sortable: true,
    sort: (a: string, b: string) => a.localeCompare(b),
    headerClasses: 'sticky-left',
    classes: 'sticky-left',
  },
  {
    name: 'track',
    field: 'track',
    label: t('track'),
    align: 'left',
  },
  {
    name: 'blocks',
    field: 'blocks',
    label: t('program_block', 9),
    align: 'left',
  },
  {
    name: 'number',
    field: 'number',
    label: t('field.number'),
    align: 'left',
    autoWidth: true,
    classes: 'panno-mono-number',
  },
  {
    name: 'email',
    field: 'email',
    label: t('field.email'),
    align: 'left',
    sortable: true,
  },
  {
    name: 'last_login',
    field: 'last_login',
    label: t('field.last_login'),
    align: 'left',
    sortable: true,
  },
];

const rows = computed(() => {
  return props.students.map((obj: StudentUser) => {
    const currentStudent = obj.student_set.find(
      (student: Student) => student.Project?.id === (project.value as Project).id
    );

    return {
      _self: obj,
      _class: currentStudent?.is_active ? '' : 'bg-red-1',
      name: obj.name,
      email: obj.email,
      track: obj.student_set[0].Track?.name || '-',
      blocks: obj.student_set.map((student) => `${student.Project?.name}-${student.Block?.name}`).join(', '),
      number: currentStudent?.number || '-',
      last_login: obj.last_login ? formatDate(obj.last_login) : '-',
    };
  });
});
</script>
