<template>
  <div v-if="formDefinition && !processing" class="q-pb-xl">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ title }}
    </h4>
    <div v-if="formDefinition.description">
      <h6 class="q-mb-md">Werkwijze</h6>
      <p>{{ formDefinition.description[locale] }}</p>
    </div>
    <div v-for="section in formDefinition.sections" :key="section.code">
      <h6 class="q-mb-none">{{ section.title[locale] }}</h6>
      <q-markup-table flat dense>
        <thead>
          <tr>
            <th></th>
            <th></th>
            <th v-for="grade in formDefinition.grades" :key="grade.value">{{ grade.label[locale] }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in section.items" :key="item.value">
            <td>{{ item.label[locale] }}</td>
            <td class="q-table--col-auto-width">
              <div class="q-px-xl">
                <q-radio
                  v-for="ci in section.cross_items"
                  :key="ci.value"
                  v-model="evaluation.data[section.code].grades[item.value][1]"
                  :disable="processing"
                  size="xs"
                  :label="ci.label[locale]"
                  :val="ci.value"
                />
              </div>
            </td>
            <td v-for="grade in formDefinition.grades" :key="grade.value" class="q-table--col-auto-width text-center">
              <q-radio
                v-model="evaluation.data[section.code].grades[item.value][0]"
                :val="grade.value"
                :disable="processing"
                size="xs"
              />
            </td>
          </tr>
          <tr v-if="formDefinition.global_section_evaluation">
            <td colspan="2" class="bg-light-blue-1">Deelscore</td>
            <td v-for="grade in formDefinition.grades" :key="grade.value" class="text-center bg-light-blue-1">
              <q-radio
                v-if="grade.value"
                v-model="evaluation.data[section.code].grade"
                :val="grade.value"
                :disable="processing"
                size="xs"
              />
            </td>
          </tr>
        </tbody>
      </q-markup-table>
      <div v-if="section.add_remarks" class="q-mt-md">
        <q-input
          v-model="evaluation.data[section.code].remarks"
          dense
          filled
          :label="$t('remark', 9)"
          type="textarea"
        />
      </div>
    </div>
    <q-markup-table flat bordered v-if="formDefinition.global_evaluation" class="q-my-lg">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th v-for="grade in completeGrades" :key="grade.value">{{ grade.label[locale] }}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td colspan="2" class="bg-light-green-1 text-left text-bold">Algemene beoordeling</td>
          <td
            v-for="grade in completeGrades"
            :key="grade.value"
            class="q-table--col-auto-width text-center bg-light-green-1"
          >
            <q-radio
              v-if="grade.value"
              v-model="evaluation.data.grade__final"
              :val="grade.value"
              :disable="sectionsWithLowGrade > 0 && grade.value > 1"
              size="xs"
            />
          </td>
        </tr>
      </tbody>
    </q-markup-table>
    <q-input v-model="evaluation.data.remarks__final" dense filled :label="title" type="textarea" />
    <q-page-sticky expand position="bottom" class="bg-white z-top">
      <div class="full-width full-height text-right q-pr-lg q-pb-lg">
        <q-separator class="q-my-lg" />
        <p v-if="sectionsWithLowGrade > 0" class="q-ml-md text-left text-body2 text-red text-bold">
          Als een of merdere deelscores een onvoldoende hebben (of geen score), kan de algemene beoordeling niet hoger
          zijn dan een onvoldoende.
        </p>
        <q-btn
          @click="saveEvaluation"
          :disable="sending || !evaluation.data.grade__final"
          unelevated
          color="ugent"
          :label="$t('form.save')"
        />
      </div>
    </q-page-sticky>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { notify } from '@/notify';

const { t, locale } = useI18n();

const props = defineProps<{
  internship: Internship;
}>();

const intermediate = {
  0: 0,
  10: 0,
  11: 1,
  20: 2,
}[props.internship.EvaluationForm?.period || 0];
const processing = ref(true);
const sending = ref(false);
const evaluation = ref({ data: {} });

const title = computed<string>(() => {
  if (intermediate > 0) {
    return t('evaluation_intermediate') + ' #' + intermediate;
  } else {
    return t('evaluation_final');
  }
});

const formDefinition = computed<EvaluationFormDefinition | undefined>(
  () => props.internship.EvaluationForm?.definition
);

/* this function adds subgrades between grades with value >, where value is something in between (one decimal) and label is always '/'. it generates a new list where we have grades and subgrades */
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
      let nextGrade = grades[i + 1];
      let newGrade = {
        label: { en: '/', nl: '/' },
        value: (grades[i].value + nextGrade.value) / 2,
      };
      newGrades.push(newGrade);
    }
  }
  return newGrades;
});
/**
 * Returns the number of sections with a low grade (== 1 or null)
 */
const sectionsWithLowGrade = computed<Record<number | null, number>>(() => {
  let count = 0;
  formDefinition.value?.sections.forEach((section) => {
    if (evaluation.value.data[section.code].grade == 1 || evaluation.value.data[section.code].grade == null) {
      count++;
    }
  });
  return count;
});

const updateEvaluationData = () => {
  processing.value = true;

  if (!evaluation.value.data.grade__final) {
    evaluation.value.data.grade__final = null;
  }

  if (!evaluation.value.data.remarks__final) {
    evaluation.value.data.remarks__final = '';
  }

  formDefinition.value?.sections.forEach((section) => {
    if (!evaluation.value.data[section.code]) {
      evaluation.value.data[section.code] = {
        grade: null,
        grades: {},
        remarks: '',
      };
    }

    section.items.forEach((item) => {
      if (!evaluation.value.data[section.code].grades[item.value]) {
        evaluation.value.data[section.code].grades[item.value] = [null, null];
      }
    });
  });

  processing.value = false;
};

function saveEvaluation() {
  sending.value = true;
  const completeData = {
    form: props.internship.EvaluationForm?.id,
    data: evaluation.value.data,
    intermediate: intermediate,
  };

  if (evaluation.value.self) {
    api
      .put(evaluation.value.self, completeData)
      .then(() => {
        notify.success(t('form.evaluation.saved'));
      })
      .finally(() => {
        sending.value = false;
      });
  } else {
    api
      .post(`${props.internship.self}evaluations/`, completeData)
      .then((res) => {
        notify.success(t('form.evaluation.create.success'));
        evaluation.value = res.data;
      })
      .finally(() => {
        sending.value = false;
      });
  }
}

function loadEvaluations() {
  api.get(`${props.internship.self}evaluations/`).then((res) => {
    // find data for this intermediate
    evaluation.value = res.data.find((obj) => obj.intermediate === intermediate) || { data: {} };
    updateEvaluationData();
  });
}

loadEvaluations();
</script>
