<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('task', 9) }}</h3>
    <div class="col"></div>
  </div>
  <student-task-box
    v-if="activeQuestionings.length && allSigned"
    :education="(education as EducationTiny)"
    :project="(project as Project)"
    :student="(student as Student)"
    :active-questionings="activeQuestionings"
    :addresses-api-endpoint="addressesApiEndpoint"
    :project-place-options="projectPlaceOptions"
    :skip-place-ids="previousPlaceIds"
    :skip-discipline-ids="previousDisciplineIds"
    class="q-mb-lg"
  />
  <div v-if="signatures !== undefined" class="q-mb-xl">
    Je wenst in het academiejaar {{ academicYear }} je {{ student.Block?.name }}-stage <strong>wel</strong> op te nemen:
    <ol>
      <li v-for="text in textsToSign" :key="text.id">
        Handtekening vereist voor <strong>{{ text.title }}</strong
        >: <a href="" v-if="!signedTextIds.has(text.id)" @click.prevent="selectedText = text">ondertekenen</a
        ><span v-else>ondertekend</span>
      </li>
    </ol>
    <q-separator class="q-my-lg" />
    Je wenst in het academiejaar {{ academicYear }} je {{ student.block.name }}-stage <strong>niet</strong> op te
    nemen.<br />Breng de stagecel hiervan op de hoogte door te mailen naar
    <a href="mailto:stagelaw@ugent.be" target="_blank">stagelaw@ugent.be</a>.
  </div>
  <q-dialog v-model="dialogVisible">
    <q-layout
      v-if="selectedText"
      view="hHh lpR fFf"
      container
      class="bg-white metis__dialog-editor"
      style="height: 600px"
    >
      <q-header class="bg-white q-pt-sm">
        <q-toolbar class="text-primary q-pl-lg q-pr-sm">
          <q-icon name="notes" />
          <q-toolbar-title>{{ selectedText.title }}</q-toolbar-title>
          <q-space />
          <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
        </q-toolbar>
      </q-header>
      <q-page-container>
        <markdown-toast-viewer
          v-model="finalText"
          :source-text="selectedText.text"
          :data="replaceData"
          class="q-px-lg"
        />
      </q-page-container>
      <q-footer class="bg-white text-dark q-pa-lg">
        <q-input
          v-model="rijksregisternummer"
          dense
          label="Rijksregisternummer *"
          mask="##.##.##-###.##"
          :rules="[(val) => val.length == 15]"
        />
        <q-list class="q-my-md">
          <q-item tag="label" v-ripple>
            <q-item-section avatar top>
              <q-checkbox v-model="acceptanceChecked" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Gelezen en goedgekeurd</q-item-label>
              <q-item-label class="text-body2">
                Handtekening - door 'Gelezen en goedgekeurd' aan te vinken en op de knop 'ondertekenen' te klikken
                onderteken je dit document en erken je uitdrukkelijk dat deze dezelfde juridische waarde heeft en
                juridisch bindend is op dezelfde manier als een origineel ondertekende versie.
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <small></small>
        <div class="flex q-gutter-sm">
          <q-space />
          <q-btn
            @click="signText"
            unelevated
            color="ugent"
            :label="$t('form.sign')"
            :disable="!acceptanceChecked || !rijksregisternummer"
          />
        </div>
      </q-footer>
    </q-layout>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import StudentTaskBox from '@/components/tasks/StudentTaskBox.vue';
import MarkdownToastViewer from '@/components/forms/MarkdownToastViewer.vue';

const { t, locale } = useI18n();
const page = usePage();
const store = useStore();

const { education, project, activeQuestionings, signatures, projectPlaceOptions } = storeToRefs(store);

const academicYear = computed<string>(() => page.props.academic_year as string);
const student = computed<Student>(() => page.props.student as Student);
const requiredTexts = computed<TextEntry[]>(() => page.props.required_texts as TextEntry[]);
const addressesApiEndpoint = computed<string>(() => (page.props.user as AuthenticatedUser)?.rel_addresses);
const previousPlaceIds = computed<number[]>(() => page.props.place_ids as number[]);
const previousDisciplineIds = computed<number[]>(() => page.props.discipline_ids as number[]);

const rijksregisternummer = ref<string>('');
const finalText = ref<string>('');

const textsToSign = computed<TextEntry[]>(() =>
  requiredTexts.value.map((text) => ({
    ...text,
    title: locale.value === 'nl' ? text.title_nl : text.title_en,
    text: locale.value === 'nl' ? text.text_nl : text.text_en,
  }))
);

const signedTextIds = computed<Set<number>>(() => {
  if (signatures.value === undefined) return new Set();
  return new Set(signatures.value.map((signature) => signature.text_entry));
});

const allSigned = computed<boolean>(() => {
  return textsToSign.value.every((text) => signedTextIds.value.has(text.id));
});

const selectedText = ref<TextEntry | null>(null);
const acceptanceChecked = ref<boolean>(false);

const dialogVisible = computed<boolean>({
  get() {
    return !!selectedText.value;
  },
  set(value) {
    if (!value) {
      selectedText.value = null;
    }
  },
});

async function signText() {
  await api
    .post('/user/student/signatures/', {
      student: student.value.id,
      text_entry: selectedText.value?.id,
      signed_text: finalText.value,
    })
    .then(() => {
      store.fetchSignatures();
      notify.success(t('form.text_entry.signed'));
      selectedText.value = null;
    });
}

const replaceData = computed(() => ({
  education_name: education.value?.short_name,
  project_academic_year: academicYear.value,
  block_name: student.value.block.name,
  student_name: student.value.user.name,
  student_rijksregisternummer: rijksregisternummer.value,
}));
</script>
