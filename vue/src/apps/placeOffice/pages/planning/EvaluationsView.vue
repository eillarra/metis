<template>
  <div v-if="formDefinition && !processing" class="q-pb-xl">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ $t('evaluation') }}
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
            <td colspan="2" class="bg-light-blue-1">Global</td>
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
    <q-page-sticky expand position="bottom" class="bg-white z-top">
      <div class="full-width full-height text-right q-pr-lg q-pb-lg">
        <q-separator class="q-mb-lg" />
        <q-btn @click="saveEvaluation" :disable="sending" unelevated color="ugent" :label="$t('form.save')" />
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

const intermediate = 1;
const processing = ref(true);
const sending = ref(false);
const evaluation = ref({ data: {} });

const formDefinition = computed<EvaluationFormDefinition | undefined>(
  () => props.internship.EvaluationForm?.definition
);

const updateEvaluationData = () => {
  processing.value = true;

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
