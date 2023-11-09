<style lang="scss">
.ugent__data-table {
  td.dense {
    width: 150px;
  }

  tfoot {
    td {
      background-color: #f5f5f5; /* bg-grey-2 */

      &.force-wrap {
        white-space: normal;
      }
    }
  }
}
</style>

<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ $t('evaluation', 9) }}
    </h4>
  </div>
  <div class="row q-col-gutter-md q-mb-lg text-right">
    <div class="col-12 col-md-3" v-for="evaluation in evaluations" :key="evaluation.id">
      <q-card flat class="bg-grey-2 q-pa-md">
        <span class="text-h5 text-ugent">
          <a :href="evaluation.url" target="_blank"><q-icon name="download" /></a>
        </span>
        <small class="float-left">{{ evaluation.name }}</small>
      </q-card>
    </div>
  </div>
  <div v-if="formDefinition">
    <q-markup-table
      v-for="section in formDefinition.sections"
      :key="section.code"
      flat
      dense
      class="ugent__data-table q-mb-md"
    >
      <thead>
        <tr>
          <th class="text-left">
            <h6 class="q-ma-none">{{ section.title.nl }}</h6>
          </th>
          <th v-for="evaluation in evaluations" :key="evaluation.id" class="text-center">
            <span v-if="evaluation.intermediate === 0">Einde</span>
            <span v-else>#{{ evaluation.intermediate }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in section.items" :key="item.value">
          <td>{{ item.label.nl }}</td>
          <td v-for="evaluation in evaluations" :key="evaluation.id" class="text-center dense">
            <span v-if="evaluation.data[section.code].grades[item.value][0]">
              {{ scoreTexts[evaluation.data[section.code].grades[item.value][0]] || '-' }}
              <q-badge
                v-if="evaluation.data[section.code].grades[item.value][1]"
                outline
                :label="evaluation.data[section.code].grades[item.value][1][0].toUpperCase() || '-'"
                color="dark"
                class="q-ml-xs"
              />
            </span>
            <span v-else>-</span>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td><small>Deelscore</small></td>
          <td v-for="evaluation in evaluations" :key="evaluation.id" class="text-center dense">
            <strong v-if="evaluation.data[section.code].grade">
              {{ scoreTexts[evaluation.data[section.code].grade] || '-' }}
            </strong>
            <span v-else>-</span>
          </td>
        </tr>
        <tr>
          <td :colspan="1 + evaluations.length" class="force-wrap bg-grey-3 text-body2">
            <p class="q-my-sm">
              <span v-for="evaluation in evaluations" :key="evaluation.id">
                <q-badge v-if="evaluation.intermediate === 0" outline color="dark">Einde</q-badge>
                <q-badge v-else outline color="dark">#{{ evaluation.intermediate }}</q-badge>
                <span class="q-ml-sm">{{ evaluation.data[section.code].remarks || '-' }}</span><br>
              </span>
            </p>
          </td>
        </tr>
      </tfoot>
    </q-markup-table>
    <q-markup-table flat dense class="ugent__data-table q-my-lg bg-light-blue-1">
      <thead>
        <tr>
          <th></th>
          <th v-for="evaluation in evaluations" :key="evaluation.id" class="text-center">
            <span v-if="evaluation.intermediate === 0">Einde</span>
            <span v-else>#{{ evaluation.intermediate }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Algemene beoordeling</strong></td>
          <td v-for="evaluation in evaluations" :key="evaluation.id" class="text-center dense text-weight-bold">
            <span v-if="evaluation.data.grade__final">
              {{ completeGradesDict[evaluation.data.grade__final].label.nl || '-' }}
            </span>
            <span v-else>-</span>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td :colspan="1 + evaluations.length" class="force-wrap bg-light-blue-2 text-body2">
            <p class="q-my-sm">
              <span v-for="evaluation in evaluations" :key="evaluation.id">
                <q-badge v-if="evaluation.intermediate === 0" outline color="dark">Einde</q-badge>
                <q-badge v-else outline color="dark">#{{ evaluation.intermediate }}</q-badge>
                <span class="q-ml-sm">{{ evaluation.data.remarks__final || '-'}}</span><br>
              </span>
            </p>
          </td>
        </tr>
      </tfoot>
    </q-markup-table>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import { api } from '@/axios.ts';

const props = defineProps<{
  internship: Internship;
}>();

const evaluations = ref<Evaluation[]>([]);
const formDefinition = computed<EvaluationFormDefinition | null>(() =>
  evaluations.value.length ? (evaluations.value[0].form_definition as EvaluationFormDefinition) : null
);

const scoreTexts = computed<Record<number, string>>(() => {
  var texts: Record<number, string> = {};
  formDefinition.value?.grades.forEach((grade) => {
    texts[grade.value] = grade.label.nl;
  });
  return texts;
});

function fetchEvaluations() {
  api.get(props.internship.rel_evaluations).then((response) => {
    evaluations.value = response.data as Evaluation[];
  });
}

onMounted(() => {
  fetchEvaluations();
});

/* this function adds subgrades between grades with value >, where value is something in between (one decimal) and label is always '/'. it generates a new list where we have grades and subgrades */
/* TODO: this is repeated so we should move it to a function */
const completeGrades = computed<Record<number | null, number>>(() => {
  const grades = formDefinition.value?.grades;

  // Initialize the new list of grades
  let newGrades: typeof grades = [];

  // Iterate over the grades
  for (let i = 0; i < grades.length; i++) {
    // If the current grade is not null, add it to the new list
    if (grades[i].value !== null) {
      newGrades.push(grades[i]);
    }

    // If it's not the last grade and both current and next grades are not null, add a new grade to the list
    if (i < grades.length - 1 && grades[i].value !== null && grades[i + 1].value !== null) {
      let prevGrade = grades[i];
      let nextGrade = grades[i + 1];
      let newGrade = {
        label: {
          en: prevGrade.label.en + ' / ' + nextGrade.label.en,
          nl: prevGrade.label.nl + ' / ' + nextGrade.label.nl,
        },
        value: (grades[i].value + nextGrade.value) / 2,
      };
      newGrades.push(newGrade);
    }
  }

  return newGrades;
});

const completeGradesDict = computed<Record<number | null, any>>(() => {
  let dict: Record<number | null, number> = {};
  completeGrades.value.forEach((grade) => {
    dict[grade.value] = grade;
  });
  return dict;
});
</script>
