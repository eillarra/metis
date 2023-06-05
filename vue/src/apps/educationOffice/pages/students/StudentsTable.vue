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
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import StudentCreateForm from './StudentCreateForm.vue';
import StudentForm from './StudentForm.vue';

const { t } = useI18n();

const props = defineProps<{
  students: StudentUser[];
}>();

const queryColumns = ['name', 'email'];

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
    name: 'email',
    field: 'email',
    label: t('field.email'),
    align: 'left',
    sortable: true,
  },
];

const rows = computed(() => {
  return props.students.map((obj: StudentUser) => {
    return {
      _self: obj,
      name: obj.name,
      email: obj.email,
      track: (obj.student_set[0].track as Track)?.name || '-',
      blocks: obj.student_set.map((stu) => `${(stu.project as Project)?.name}-${stu.block?.name}`).join(', '),
    };
  });
});
</script>
