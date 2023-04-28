<template>
  <data-table
    :title="$t('student', 10)"
    :loading="loading"
    :rows="rows"
    :columns="columns"
    :query-columns="queryColumns"
    sort-by="name"
  >
    <template #filters>
      <q-select
        dense
        square
        outlined
        v-model="selectedBlock"
        :options="blockFilters"
        label="Filter groups"
        clearable
        options-dense
        emit-value
        map-options
        class="col-12 col-md-3"
      >
        <template #prepend>
          <q-icon name="filter_alt" />
        </template>
      </q-select>
    </template>
  </data-table>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, toRefs, watch, Ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import DataTable from '@/components/DataTable.vue';

const { t } = useI18n();

const props = defineProps<{
  project: Project;
  programs: Program[] | null;
}>();

const loading: Ref<boolean> = ref(true);
const { project } = toRefs(props);
const students: Ref<Student[]> = ref([]);
const queryColumns = ['name', 'email'];

const blockFilters = computed(() => {
  if (!props.programs) {
    return [];
  }

  return props.programs.reduce((acc: object[], program: Program) => {
    return [
      ...acc,
      ...program.blocks.map((block: ProgramBlockTiny) => {
        return {
          value: block.id,
          label: `${program.name} ${block.name}`,
        };
      }),
    ];
  }, []);
});

const selectedBlock: Ref<number | null> = ref(null);

async function fetchStudents() {
  loading.value = true;
  students.value = [];

  await api
    .get(project.value.rel_students)
    .then((response) => {
      students.value = response.data;
    })
    .finally(() => {
      loading.value = false;
    });
}

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
    label: t('field.program_blocks'),
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
  return students.value
    .filter((student) =>
      selectedBlock.value
        ? student.student_records.some(
            (rec) => rec.project.id == project.value.id && rec.block.id == selectedBlock.value
          )
        : student.student_records.some((rec) => rec.project.id == project.value.id)
    )
    .map((student) => ({
      name: `${student.first_name} ${student.last_name}`,
      email: student.email,
      blocks: student.student_records.map((rec) => `${rec.project.name}-${rec.block.name}`).join(', '),
    }));
});

onMounted(() => {
  fetchStudents();
});

watch(project, fetchStudents);
</script>
