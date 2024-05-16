<template>
  <div v-if="!loading && !currentPeriod">
    <big-message :text="$t('form.evaluation.not_available')" icon="event_busy" />
    <div class="text-center">
      Evaluation periods:<br />
      <span v-for="period in evaluationPeriods" :key="period.intermediate">
        <strong>{{ period.name }}</strong
        >: {{ period.start }} - {{ period.end }}<br />
      </span>
    </div>
  </div>
  <div v-else-if="!loading">
    <div v-if="formDefinition && evaluation && !processing" class="q-pb-xl">
      <div v-if="currentPeriod">
        <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
          {{ currentPeriod.name }} (<span v-if="l == 'nl'">rond</span><span v-else>around</span>
          {{ currentPeriod.deadline }})
          <q-badge v-if="!evaluation.is_approved" color="orange" class="q-ml-sm" style="vertical-align: middle">{{
            $t('draft')
          }}</q-badge>
        </h4>
        <!--<small>Evaluatieperiode: {{ currentPeriod.start }} - {{ currentPeriod.end }}</small>-->
      </div>
      <div v-if="evaluation.is_approved">
        <big-message :text="$t('form.evaluation.approved')" icon="done_outline" />
      </div>
      <div v-else>
        <div v-for="section in formDefinition.sections" :key="section.code">
          <h6 v-if="section.title" class="q-mb-none">{{ section.title[l] }}</h6>
          <q-markup-table flat dense class="full-width">
            <thead>
              <tr>
                <th></th>
                <th></th>
                <th v-for="score in sectionScores" :key="score.value">{{ score.label[l] }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in section.items" :key="item.value">
                <td class="q-pt-lg" style="text-wrap: wrap; padding: 10px !important">
                  <q-icon
                    v-show="item.score_help_texts"
                    @click="expandedItem = expandedItem == item.value ? null : item.value"
                    :name="expandedItem == item.value ? 'expand_less' : 'help_outline'"
                    size="13px"
                    class="q-mb-xs cursor-pointer"
                  ></q-icon
                  >&nbsp;&nbsp;&nbsp;{{ item.label[l] }}
                  <ul v-show="expandedItem == item.value" style="text-wrap: balance">
                    <li v-for="ht in item.score_help_texts" :key="ht[0]" class="q-py-none">
                      <strong>{{ scoreTexts[ht[0]] }}:</strong> {{ ht[1][l] }}
                    </li>
                  </ul>
                </td>
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
              <tr v-if="section.with_score">
                <td colspan="2" class="bg-light-blue-1">{{ $t('section_score') }}</td>
                <td v-for="score in sectionScores" :key="score.value" class="text-center bg-light-blue-1">
                  <q-radio
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
              <td colspan="2" class="bg-light-green-1 text-left text-bold">{{ $t('global_score') }}</td>
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
        <div v-if="asSelfEvaluation">
          <h6 class="text-weight-bold">{{ $t('report') }}</h6>
          <markdown-toast-editor v-model="evaluation.data.global_remarks" />
        </div>
        <q-input
          v-else
          v-model="evaluation.data.global_remarks"
          dense
          filled
          :label="currentPeriod?.name"
          type="textarea"
          style="margin-bottom: 100px;"
        />
        <q-page-sticky expand position="bottom" class="bg-white z-top">
          <div class="full-width full-height text-right q-pr-lg q-pb-lg">
            <q-separator class="q-my-lg" />
            <p v-if="sectionsWithLowScore > 0" class="q-ml-md text-left text-body1 text-red text-bold">
              Als een of merdere deelscores een onvoldoende hebben (of geen score), kan de algemene beoordeling niet
              hoger zijn dan een onvoldoende.
            </p>
            <div class="q-gutter-sm">
              <q-btn
                v-if="evaluation.self"
                unelevated
                color="blue-1"
                :label="`&nbsp;${$t('form.evaluation.approve')}`"
                icon="done_outline"
                class="text-ugent"
                :disable="evaluation.is_approved || sectionsWithLowScore > 0"
                @click="signatureVisible = true"
              />
              <q-btn
                @click="saveEvaluation"
                :disable="sending || !evaluation.data.global_score || evaluation.is_approved"
                unelevated
                color="ugent"
                :label="$t('form.save')"
              />
              <signature-dialog
                v-if="evaluation.self"
                v-model="signatureVisible"
                :title="$t('form.evaluation.approve')"
                :text-to-sign="textToSign"
                :callback="approveEvaluation"
              />
            </div>
          </div>
        </q-page-sticky>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { usePage } from '@inertiajs/vue3';

import { api } from '@/axios.ts';
import { notify } from '@/notify';
import { formatDate } from '@/utils/dates';

import BigMessage from '@/components/BigMessage.vue';
import SignatureDialog from '@/components/SignatureDialog.vue';
import MarkdownToastEditor from '@/components/forms/MarkdownToastEditor.vue';

const { t, locale } = useI18n();

const props = defineProps<{
  internship: Internship;
  asSelfEvaluation?: boolean;
}>();

// --
const page = usePage();
const djangoUser = computed<DjangoAuthenticatedUser>(() => page.props.django_user as DjangoAuthenticatedUser);
// --

const l = ref<'en' | 'nl'>(locale.value as 'en' | 'nl');
const loading = ref<boolean>(true);
const asSelfEvaluation = props.internship.EvaluationForm?.has_self_evaluations && props.asSelfEvaluation;
const signatureVisible = ref<boolean>(false);

const evaluations = ref<Evaluation[]>([]);
const evaluationPeriods = ref<EvaluationPeriod[]>(
  props.internship.evaluation_periods?.map((period) => {
    const intermediateText = props.asSelfEvaluation ? t('self_evaluation_intermediate') : t('evaluation_intermediate');
    const finalText = props.asSelfEvaluation ? t('self_evaluation_final') : t('evaluation_final');

    return {
      intermediate: period[0],
      name: period[0] > 0 ? intermediateText + ' #' + period[0] : finalText,
      is_final: period[0] == 0,
      start_at: new Date(period[1]),
      end_at: new Date(period[2]),
      start: formatDate(period[1]),
      end: formatDate(period[2]),
      deadline: formatDate(period[3], 'YYYY-MM-DD'),
    };
  }) || []
);

const currentPeriod = ref<EvaluationPeriod | null>();

const processing = ref(true);
const sending = ref(false);
const evaluation = ref<Evaluation>();
const expandedItem = ref<string | null>(null);

const formDefinition = computed<EvaluationFormDefinition | undefined>(
  () => props.internship.EvaluationForm?.definition
);

const sectionScores = computed<EvaluationScore[]>(() => {
  return formDefinition.value?.scores.filter((score) => !score.only_for_global_score) || [];
});

const scoreTexts = computed<Record<number, string>>(() => {
  var texts: Record<number, string> = {};
  formDefinition.value?.scores.forEach((score: EvaluationScore) => {
    texts[score.value] = score.label[l.value];
  });
  return texts;
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
  if (evaluation.value?.data.global_score == lowestScore.value?.value) {
    // we don't care if the final evaluation is the lowest possible anyway
    return 0;
  }

  let count = 0;

  formDefinition.value?.sections.forEach((section) => {
    if (
      section.with_score &&
      (evaluation.value?.data.sections[section.code].score == lowestScore.value?.value ||
        evaluation.value?.data.sections[section.code].score === undefined)
    ) {
      count++;
    }
  });

  return count;
});

const textToSign = computed<string>(() => {
  let text = `Ondergetekende,

${djangoUser.value.first_name} ${djangoUser.value.last_name} (${djangoUser.value.email}) medewerker op stageplaats ${
    props.internship.Place?.name
  } bevestigt dat student ${props.internship.Student?.User?.name} met studentennummer ${
    props.internship.Student?.number
  } een score van **"${
    scoreTexts.value[(evaluation.value?.data.global_score ?? -1) as number] || '-'
  }"** heeft behaald voor de **${currentPeriod.value?.name}**.
`;

  let textEn = `The undersigned,

${djangoUser.value.first_name} ${djangoUser.value.last_name} (${djangoUser.value.email}) employee at ${
    props.internship.Place?.name
  } confirms that student ${props.internship.Student?.User?.name} with student number ${
    props.internship.Student?.number
  } has achieved a score of **"${
    scoreTexts.value[(evaluation.value?.data.global_score ?? -1) as number] || '-'
  }"** for the **${currentPeriod.value?.name}**.
`;

  let textStudent = `Ondergetekende,

${props.internship.Student?.User?.name} met studentennummer ${props.internship.Student?.number} bevestigt de ingediende evaluatie voor de **${currentPeriod.value?.name}**.
`;

  let textStudentEn = `The undersigned,

${props.internship.Student?.User?.name} with student number ${props.internship.Student?.number} confirms the submitted evaluation for the **${currentPeriod.value?.name}**.
`;

  if (asSelfEvaluation) {
    text = textStudent;
    textEn = textStudentEn;
  }

  return l.value == 'en' ? textEn : text;
});

const updateEvaluationData = () => {
  processing.value = true;

  if (!evaluation.value) {
    evaluation.value = {
      self: '',
      data: {
        global_remarks: '',
        global_score: undefined,
        sections: {},
      },
    } as Evaluation;
  }

  formDefinition.value?.sections.forEach((section) => {
    if (!(evaluation.value as Evaluation).data.sections[section.code]) {
      (evaluation.value as Evaluation).data.sections[section.code] = {
        remarks: '',
        score: undefined,
        scores: {},
      };
    }

    section.items.forEach((item) => {
      if (!(evaluation.value as Evaluation).data.sections[section.code].scores[item.value]) {
        (evaluation.value as Evaluation).data.sections[section.code].scores[item.value] = [null, null];
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
    intermediate: currentPeriod.value?.intermediate || 0,
    is_self_evaluation: props.asSelfEvaluation || false,
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

function approveEvaluation() {
  sending.value = true;

  if (evaluation.value?.is_approved) {
    return;
  }

  if (evaluation.value?.self) {
    api
      .post(`${evaluation.value.self}approve/`, { signed_text: textToSign.value })
      .then(() => {
        notify.success(t('form.evaluation.approved'));
        if (evaluation.value) {
          evaluation.value.is_approved = true;
        }
      })
      .finally(() => {
        sending.value = false;
      });
  }
}

function loadEvaluations() {
  api.get(`${props.internship.self}evaluations/`).then((res) => {
    evaluations.value = res.data as Evaluation[];

    /* calculate current period: this is the period that matches dates, OR the first one that is not submitted */
    currentPeriod.value = evaluationPeriods.value.find(
      (period) =>
        !evaluations.value.find(
          (evaluation) => evaluation.intermediate === period.intermediate && evaluation.is_approved
        ) || // not submitted and approved
        (period.start_at <= new Date() && period.end_at >= new Date()) // current period
    );

    loading.value = false;

    evaluation.value = res.data.find(
      (obj: Evaluation) =>
        obj.intermediate === currentPeriod.value?.intermediate && obj.is_self_evaluation == asSelfEvaluation
    );
    updateEvaluationData();
  });
}

loadEvaluations();
</script>
