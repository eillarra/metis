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
  <div class="row q-col-gutter-md q-mb-lg">
    <div class="col-12 col-md-3" v-for="evaluation in evaluations" :key="evaluation.id">
      <q-card flat class="bg-grey-2 q-pa-md metis__dashcard">
        <a v-if="evaluation.is_approved" :href="evaluation.url" target="_blank" class="text-h5 text-ugent float-right">
          <q-icon name="download" />
        </a>
        <q-icon v-else name="draw" class="text-h5 text-grey float-right cursor-help">
          <q-tooltip :delay="250">{{ $t('draft') }}</q-tooltip>
        </q-icon>
        <small>{{ evaluation.name }}<strong v-if="!evaluation.is_approved"></strong></small>
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
            <h6 v-if="section.title" class="q-ma-none">{{ section.title[l] }}</h6>
          </th>
          <th v-for="evaluation in evaluations" :key="evaluation.id" class="text-center">
            <span v-if="evaluation.intermediate === 0">Einde</span>
            <span v-else>#{{ evaluation.intermediate }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in section.items" :key="item.value">
          <td>{{ item.label[l] }}</td>
          <td
            v-for="evaluation in evaluations"
            :key="evaluation.id"
            class="text-center dense"
            :class="{ 'text-grey': !evaluation.is_approved }"
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
      <tfoot>
        <tr>
          <td><small>Deelscore</small></td>
          <td
            v-for="evaluation in evaluations"
            :key="evaluation.id"
            class="text-center dense"
            :class="{ 'text-grey': !evaluation.is_approved }"
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
              <span v-for="evaluation in evaluations" :key="evaluation.id">
                <q-badge v-if="evaluation.intermediate === 0" outline color="dark">Einde</q-badge>
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
            <span v-if="evaluation.data.global_score && evaluation.is_approved">
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
              <span v-for="evaluation in evaluations" :key="evaluation.id">
                <q-badge v-if="evaluation.intermediate === 0" outline color="dark">Einde</q-badge>
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
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';

const { locale } = useI18n();

const props = defineProps<{
  internship: Internship;
  showPoints?: boolean;
}>();

const l = ref<'en' | 'nl'>(locale.value as 'en' | 'nl');
const evaluations = ref<Evaluation[]>([]);
const formDefinition = computed<EvaluationFormDefinition | null>(() =>
  evaluations.value.length ? (evaluations.value[0].form_definition as EvaluationFormDefinition) : null
);
const pointsToggle = ref<boolean>(false);

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
  });
}

onMounted(() => {
  fetchEvaluations();
});
</script>
