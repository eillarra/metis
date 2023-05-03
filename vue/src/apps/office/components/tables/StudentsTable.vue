<template>
  <data-table
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    :form-component="StudentForm"
    sort-by="name"
  />
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue';
import { useI18n } from 'vue-i18n';

import DataTable from '@/components/tables/DataTable.vue';
import StudentForm from '../forms/StudentForm.vue';

const { t } = useI18n();

const props = defineProps<{
  students: Student[];
}>();

const { students } = toRefs(props);
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
  return students.value.map((user) => ({
    _self: user,
    name: user.name,
    email: user.email,
    blocks: user.student_objects.map((rec) => `${rec.project.name}-${rec.block.name}`).join(', '),
  }));
});
</script>
