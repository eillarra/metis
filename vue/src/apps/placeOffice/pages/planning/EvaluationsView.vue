<template>
  <div v-if="formDefinition && evaluation && !processing" class="q-pb-xl">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ title }}
    </h4>
    <div v-if="formDefinition.description">
      <h6 class="q-mb-md">Werkwijze</h6>
      <p>{{ formDefinition.description[l] }}</p>
    </div>
    <div v-for="section in formDefinition.sections" :key="section.code">
      <h6 v-if="section.title" class="q-mb-none">{{ section.title[l] }}</h6>
      <q-markup-table flat dense>
        <thead>
          <tr>
            <th></th>
            <th></th>
            <th v-for="score in sectionScores" :key="score.value">{{ score.label[l] }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in section.items" :key="item.value">
            <td>{{ item.label[l] }}</td>
            <td class="q-table--col-auto-width">
              <div class="q-px-xl">
                <q-radio
                  v-for="ci in section.cross_items"
                  :key="ci.value"
                  v-model="evaluation.data.sections[section.code].scores[item.value][1]"
                  :disable="processing"
                  size="xs"
                  :label="ci.label[l]"
                  :val="ci.value"
                />
              </div>
            </td>
            <td v-for="score in sectionScores" :key="score.value" class="q-table--col-auto-width text-center">
              <q-radio
                v-model="evaluation.data.sections[section.code].scores[item.value][0]"
                :val="score.value"
                :disable="processing"
                size="xs"
              />
            </td>
          </tr>
          <tr>
            <td colspan="2" class="bg-light-blue-1">Deelscore</td>
            <td v-for="score in sectionScores" :key="score.value" class="text-center bg-light-blue-1">
              <q-radio
                v-if="score.value"
                v-model="evaluation.data.sections[section.code].score"
                :val="score.value"
                :disable="processing"
                size="xs"
              />
            </td>
          </tr>
        </tbody>
      </q-markup-table>
      <div v-if="section.with_remarks" class="q-mt-md">
        <q-input
          v-model="evaluation.data.sections[section.code].remarks"
          dense
          filled
          :label="$t('remark', 9)"
          type="textarea"
        />
      </div>
    </div>
    <q-markup-table flat bordered class="q-my-lg">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th v-for="score in formDefinition.scores" :key="score.value">
            <span v-if="score.only_for_global_score">/</span>
            <span v-else-if="score.value">{{ score.label[l] }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td colspan="2" class="bg-light-green-1 text-left text-bold">Algemene beoordeling</td>
          <td
            v-for="score in formDefinition.scores"
            :key="score.value"
            class="q-table--col-auto-width text-center bg-light-green-1"
          >
            <q-radio
              v-if="score.value && score.points"
              v-model="evaluation.data.global_score"
              :val="score.value"
              :disable="sectionsWithLowScore > 0 && score.points > (lowestScore?.points || 0)"
              size="xs"
            />
          </td>
        </tr>
      </tbody>
    </q-markup-table>
    <q-input v-model="evaluation.data.global_remarks" dense filled :label="title" type="textarea" />
    <q-page-sticky expand position="bottom" class="bg-white z-top">
      <div class="full-width full-height text-right q-pr-lg q-pb-lg">
        <q-separator class="q-my-lg" />
        <p v-if="sectionsWithLowScore > 0" class="q-ml-md text-left text-body1 text-red text-bold">
          Als een of merdere deelscores een onvoldoende hebben (of geen score), kan de algemene beoordeling niet hoger
          zijn dan een onvoldoende.
        </p>
        <q-btn
          @click="saveEvaluation"
          :disable="sending || !evaluation.data.global_score"
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

const l = ref<'en' | 'nl'>(locale.value as 'en' | 'nl');
const intermediate = {
  /* temporary */ // TODO: remove
  0: 0,
  10: 0,
  11: 1,
  20: 2,
}[props.internship.EvaluationForm?.period || 0] as 0 | 1 | 2;
const processing = ref(true);
const sending = ref(false);
const evaluation = ref<Evaluation>();

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

const sectionScores = computed<EvaluationScore[]>(() => {
  return formDefinition.value?.scores.filter((score) => !score.only_for_global_score) || [];
});

/**
 * Returns the lowest score that is not null
 */
const lowestScore = computed<EvaluationScore | null>(() => {
  let lowestScore: EvaluationScore | null = null;

  formDefinition.value?.scores.forEach((score: EvaluationScore) => {
    if (score.points && (!lowestScore || (lowestScore.points !== null && score.points < lowestScore.points))) {
      lowestScore = score;
    }
  });

  return lowestScore;
});

/**
 * Returns the number of sections with a low score (== 'onv' or null)
 */
const sectionsWithLowScore = computed<number>(() => {
  let count = 0;
  formDefinition.value?.sections.forEach((section) => {
    if (
      evaluation.value?.data.sections[section.code].score == lowestScore.value?.value ||
      evaluation.value?.data.sections[section.code].score == null
    ) {
      count++;
    }
  });
  return count;
});

const updateEvaluationData = () => {
  processing.value = true;

  if (!evaluation.value) {
    evaluation.value = {
      self: '',
      data: {
        global_remarks: '',
        global_score: null,
        sections: {},
      },
      intermediate: intermediate,
    };
  }

  formDefinition.value?.sections.forEach((section) => {
    if (!evaluation.value.data.sections[section.code]) {
      evaluation.value.data.sections[section.code] = {
        remarks: '',
        score: null,
        scores: {},
      };
    }

    section.items.forEach((item) => {
      if (!evaluation.value.data.sections[section.code].scores[item.value]) {
        evaluation.value.data.sections[section.code].scores[item.value] = [null, null];
      }
    });
  });

  processing.value = false;
};

function saveEvaluation() {
  sending.value = true;
  const completeData = {
    form: props.internship.EvaluationForm?.id,
    data: evaluation.value?.data,
    intermediate: intermediate,
  };

  if (evaluation.value?.self) {
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
    evaluation.value = res.data.find((obj: Evaluation) => obj.intermediate === intermediate);
    updateEvaluationData();
  });
}

loadEvaluations();
</script>
