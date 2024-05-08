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
  <div class="row q-col-gutter-lg q-mb-none">
    <h4 class="col-12 col-md-6 q-mt-none q-mb-lg">
      {{ $t('evaluation', 9) }}
    </h4>
    <div v-if="props.showPoints" class="col-12 col-md text-right ugent__create-btn">
      <q-btn unelevated color="blue-1" class="text-ugent">
        <q-toggle v-model="pointsToggle" :label="$t('form.evaluation.show_points')" class="q-pr-md" />
      </q-btn>
    </div>
  </div>
  <div class="bg-yellow-1">
    <ul class="q-py-sm q-mt-xs">
      <li v-for="period in internship.evaluation_periods" :key="period[0]">
        <span v-if="period[0] > 0">#{{ period[0] }}</span
        ><span v-else>Einde</span>: <strong>{{ period[3] }}</strong> (invullen tussen {{ formatDate(period[1]) }} en
        {{ formatDate(period[2]) }})
      </li>
    </ul>
  </div>
  <q-tabs v-if="evaluationTypes.length > 1" v-model="tab">
    <q-tab
      v-for="etype in evaluationTypes"
      :key="etype"
      :name="`tab_${etype}`"
      :label="etype === 0 ? $t('place') : $t('self_evaluation')"
    />
  </q-tabs>
  <q-tab-panels v-model="tab" animated>
    <q-tab-panel v-for="etype in evaluationTypes" :key="etype" :name="`tab_${etype}`" class="q-pa-none">
      <div v-if="!loading && (groupedEvaluations[etype] || []).length == 0">
        <big-message :text="$t('form.evaluation.not_found')" icon="remove_done" />
        <div v-if="showPeriods" class="text-center">
          {{ $t('evaluation_period', 9) }}:<br />
          <span v-for="period in evaluationPeriods" :key="period.intermediate">
            <strong>{{ period.name }}</strong
            >: {{ period.start }} - {{ period.end }}<br />
          </span>
        </div>
      </div>
      <div v-else class="row q-col-gutter-md q-mb-lg">
        <div class="col-12 col-md-3" v-for="evaluation in groupedEvaluations[etype] || []" :key="evaluation.id">
          <q-card flat class="bg-grey-2 q-pa-md metis__dashcard">
            <a
              v-if="evaluation.is_approved"
              :href="evaluation.url"
              target="_blank"
              class="text-h5 text-ugent float-right"
            >
              <q-icon name="download" />
            </a>
            <q-icon v-else name="draw" class="text-h5 text-orange-8 float-right cursor-help">
              <q-tooltip :delay="250">{{ $t('draft') }}</q-tooltip>
            </q-icon>
            <small>{{ evaluation.name }}<strong v-if="!evaluation.is_approved"></strong></small>
          </q-card>
        </div>
      </div>
      <div v-if="formDefinition && (groupedEvaluations[etype] || []).length">
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
                <h6 v-if="section.title" class="q-ma-none">{{ section.title[l] }}</h6>
              </th>
              <th v-for="evaluation in groupedEvaluations[etype] || []" :key="evaluation.id" class="text-center">
                <span v-if="evaluation.intermediate === 0">{{ $t('evaluation_final') }}</span>
                <span v-else>#{{ evaluation.intermediate }}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in section.items" :key="item.value">
              <td>{{ item.label[l] }}</td>
              <td
                v-for="evaluation in groupedEvaluations[etype] || []"
                :key="evaluation.id"
                class="text-center dense"
                :class="{ 'text-orange-8': !evaluation.is_approved }"
              >
                <span
                  v-if="
                    evaluation.data.sections[section.code].scores[item.value] &&
                    evaluation.data.sections[section.code].scores[item.value][0]
                  "
                >
                  {{ scoreTexts[evaluation.data.sections[section.code].scores[item.value][0]] || '-' }}
                  <q-badge
                    v-if="evaluation.data.sections[section.code].scores[item.value][1]"
                    outline
                    :label="(evaluation.data.sections[section.code].scores[item.value][1] as string)[0].toUpperCase() || '-'"
                    color="dark"
                    class="q-ml-xs"
                  />
                </span>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
          <tfoot v-if="section.with_score">
            <tr>
              <td class="bg-grey-1"><small>Deelscore</small></td>
              <td
                v-for="evaluation in groupedEvaluations[etype] || []"
                :key="evaluation.id"
                class="text-center dense bg-grey-1"
                :class="{ 'text-orange-8': !evaluation.is_approved }"
              >
                <strong v-if="evaluation.data.sections[section.code].score">
                  {{ scoreTexts[evaluation.data.sections[section.code].score] || '-' }}
                </strong>
                <span v-else>-</span>
              </td>
            </tr>
            <tr v-if="section.with_remarks">
              <td :colspan="1 + evaluations.length" class="force-wrap bg-grey-3 text-body2">
                <p class="q-my-sm">
                  <span v-for="evaluation in groupedEvaluations[etype] || []" :key="evaluation.id">
                    <q-badge v-if="evaluation.intermediate === 0" outline color="dark">{{
                      $t('evaluation_final')
                    }}</q-badge>
                    <q-badge v-else outline color="dark">#{{ evaluation.intermediate }}</q-badge>
                    <span class="q-ml-sm">{{ evaluation.data.sections[section.code].remarks || '-' }}</span>
                    <br />
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
              <th v-for="evaluation in groupedEvaluations[etype] || []" :key="evaluation.id" class="text-center">
                <span v-if="evaluation.intermediate === 0">{{ $t('evaluation_final') }}</span>
                <span v-else>#{{ evaluation.intermediate }}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Algemene beoordeling</strong></td>
              <td
                v-for="evaluation in groupedEvaluations[etype] || []"
                :key="evaluation.id"
                class="text-center dense text-weight-bold"
                :class="{ 'text-orange-8': !evaluation.is_approved }"
              >
                <span v-if="evaluation.data.global_score">
                  {{ scoreTexts[evaluation.data.global_score] || '-' }}
                </span>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td :colspan="1 + evaluations.length" class="force-wrap bg-light-blue-2 text-body2">
                <p class="q-my-sm">
                  <span v-for="evaluation in groupedEvaluations[etype] || []" :key="evaluation.id">
                    <q-badge v-if="evaluation.intermediate === 0" outline color="dark">{{
                      $t('evaluation_final')
                    }}</q-badge>
                    <q-badge v-else outline color="dark">#{{ evaluation.intermediate }}</q-badge>
                    <span class="q-ml-sm">{{ evaluation.data.global_remarks || '-' }}</span>
                    <br />
                  </span>
                </p>
              </td>
            </tr>
          </tfoot>
        </q-markup-table>
      </div>
    </q-tab-panel>
  </q-tab-panels>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { formatDate } from '@/utils/dates';

import BigMessage from '@/components/BigMessage.vue';

const { t, locale } = useI18n();

const props = defineProps<{
  internship: Internship;
  showPoints?: boolean;
  showPeriods?: boolean;
}>();

const l = ref<'en' | 'nl'>(locale.value as 'en' | 'nl');
const loading = ref<boolean>(true);
const tab = ref<string>('tab_0');
const evaluations = ref<Evaluation[]>([]);
const formDefinition = computed<EvaluationFormDefinition | null>(() =>
  evaluations.value.length ? (evaluations.value[0].form_definition as EvaluationFormDefinition) : null
);
const hasSelfEvaluations = computed<boolean>(() =>
  evaluations.value.find((evaluation) => evaluation.is_self_evaluation) ? true : false
);
const evaluationTypes = computed<number[]>(() => (hasSelfEvaluations.value ? [0, 1] : [0]));
const groupedEvaluations = computed<Record<number, Evaluation[]>>(() => {
  // convert list of evaluations to
  // object with is_self_evaluation as key
  return evaluations.value.reduce((acc, evaluation) => {
    if (!acc[+evaluation.is_self_evaluation]) {
      acc[+evaluation.is_self_evaluation] = [];
    }
    acc[+evaluation.is_self_evaluation].push(evaluation);
    return acc;
  }, {} as Record<number, Evaluation[]>);
});

const pointsToggle = ref<boolean>(false);
const evaluationPeriods = ref<EvaluationPeriod[]>(
  !props.showPeriods
    ? []
    : props.internship.evaluation_periods?.map((period) => {
        return {
          intermediate: period[0],
          name: period[0] > 0 ? t('evaluation_intermediate') + ' #' + period[0] : t('evaluation_final'),
          is_final: period[0] == 0,
          start_at: new Date(period[1]),
          end_at: new Date(period[2]),
          start: formatDate(period[1]),
          end: formatDate(period[2]),
        };
      }) || []
);

const scoreTexts = computed<Record<number, string>>(() => {
  var texts: Record<number, string> = {};
  formDefinition.value?.scores.forEach((score: EvaluationScore) => {
    texts[score.value] = pointsToggle.value ? `${score.points}` || '-' : score.label[l.value];
  });
  return texts;
});

function fetchEvaluations() {
  api.get(props.internship.rel_evaluations).then((response) => {
    evaluations.value = response.data as Evaluation[];
    loading.value = false;
  });
}

onMounted(() => {
  fetchEvaluations();
});
</script>
