<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('task', 9) }}</h3>
    <div class="col"></div>
  </div>
  <div v-show="signatures !== undefined" class="q-mb-xl">
    Je wenst in het academiejaar {{ academicYear }} je {{ student.block.name }}-stage <strong>wel</strong> op te nemen:
    <ol>
      <li v-for="text in textsToSign" :key="text.id">
        Handtekening vereist voor <strong>{{ text.title }}</strong
        >: <a href v-if="!signedTextIds.has(text.id)" @click.prevent="selectedText = text">ondertekenen</a
        ><span v-else>ondertekend</span>
      </li>
      <li>
        Werk uw persoonlijke informatie bij:
        <a href :class="{ disabled: !allSigned }" @click.prevent="formDialogVisible = allSigned">hier</a>
      </li>
    </ol>
    Je hebt hiertoe tijd tot zondag 4 juni 2023 23:59.
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
          v-model="tmpData.rijksregisternummer"
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
            :disable="!acceptanceChecked || !tmpData.rijksregisternummer"
          />
        </div>
      </q-footer>
    </q-layout>
  </q-dialog>
  <q-dialog v-model="formDialogVisible">
    <q-layout view="hHh lpR fFf" container class="bg-white metis__dialog-editor" style="height: 600px">
      <q-header class="bg-white q-pt-sm">
        <q-toolbar class="text-primary q-pl-lg q-pr-sm">
          <q-icon name="notes" />
          <q-toolbar-title>{{ student.user.name }}</q-toolbar-title>
          <q-space />
          <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
        </q-toolbar>
      </q-header>
      <q-page-container>
        <div class="row q-px-lg q-py-md">
          <q-input
            v-model="tmpData.rijksregisternummer"
            dense
            label="Rijksregisternummer"
            class="col-12"
            mask="##.##.##-###.##"
            :rules="[(val) => val.length == 15]"
          />
          <q-input v-model="tmpData.mobile_phone" dense label="Telefoonnummer" class="col-12" mask="#### ## ## ##" />
          <h6 class="q-mt-lg q-mb-sm">Domicilieadres</h6>
          <q-input v-model="tmpData.address" dense label="Address" class="col-12 q-mb-sm" />
          <q-input v-model="tmpData.city" dense label="Stad" class="col-12 q-mb-sm" />
          <q-checkbox
            v-model="extraAdress"
            label="Logeeradres elders in Belgie dat kan fungeren als uitvalsbasis tijdens stage"
          />
          <q-input v-show="extraAdress" v-model="tmpData.address2" dense label="Address" class="col-12 q-mb-sm" />
          <q-input v-show="extraAdress" v-model="tmpData.city2" dense label="Stad" class="col-12 q-mb-sm" />
          <q-checkbox v-model="tmpData.has_kot" label="Kot in Gent" class="col-12" />
          <h6 class="q-mt-lg q-mb-sm">Stages</h6>
          <q-checkbox
            v-model="tmpData.is_interested_in_foreign"
            label="Interesse in stage NL/Wallonie"
            class="col-12"
          />
          <q-checkbox v-model="tmpData.has_car" label="Beschikbaarheid auto" class="col-12" />
          <q-checkbox
            v-model="tmpData.can_speak_french"
            label="Tweetalig en/of voldoende kennis Frans"
            class="col-12"
          />
          <q-input
            v-show="tmpData.can_speak_french"
            v-model="tmpData.can_speak_details"
            dense
            label="Specifiëren aub"
            class="col-12 q-mb-sm"
          />
          <h6 class="q-mt-lg q-mb-sm">Andere</h6>
          <q-checkbox v-model="tmpData.has_special_status" label="Bijzonder statuut" class="col-12" />
          <q-checkbox v-model="tmpData.is_werkstudent" label="Werkstudent" class="col-12" />
          <q-checkbox v-model="tmpData.is_beursstudent" label="Beursstudent" class="col-12" />
          <q-input v-model="tmpData.comments" type="text" label="Opmerkingen" class="col-12" autogrow />
        </div>
      </q-page-container>
      <q-footer class="bg-white text-dark q-pa-lg">
        <div class="flex q-gutter-sm">
          <q-space />
          <q-btn
            @click="saveTmpData"
            unelevated
            color="ugent"
            :label="$t('form.update')"
            :disable="!tmpData.rijksregisternummer || !tmpData.address || !tmpData.city"
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

import MarkdownToastViewer from '@/components/forms/MarkdownToastViewer.vue';

const { t, locale } = useI18n();
const page = usePage();
const store = useStore();

const { education, signatures } = storeToRefs(store);

const academicYear = computed<string>(() => page.props.academic_year as string);
const student = computed<Student>(() => page.props.student as Student);
const requiredTexts = computed<TextEntry[]>(() => page.props.required_texts as TextEntry[]);

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
    .then((res) => {
      store.fetchSignatures();
      notify.success(t('form.text_entry.signed'));
      selectedText.value = null;
    });
}

/**
 * Replace handlebars in text with values from the student
 * -------------------------------------------------------
 * CHECK LATER AGAIN
 * -------------------------------------------------------
 */

const formDialogVisible = ref<boolean>(false);

const extraAdress = ref<boolean>(false);
const tmpDataExists = ref<boolean>(page.props.user?.tmp_data !== null);
const tmpData = ref<object>(
  page.props.user?.tmp_data || {
    rijksregisternummer: '',
    address: '',
    city: '',
    address2: '',
    city2: '',
    has_kot: false,
    has_car: false,
    has_special_status: false,
    can_speak_french: false,
    can_speak_details: '',
    is_interested_in_foreign: false,
    is_werkstudent: false,
    is_beursstudent: false,
    comments: '',
    mobile_phone: '',
  }
);

const replaceData = computed(() => ({
  education_name: education.value?.short_name,
  project_academic_year: academicYear.value,
  block_name: student.value.block.name,
  student_name: student.value.user.name,
  student_rijksregisternummer: tmpData.value.rijksregisternummer,
}));

async function saveTmpData() {
  if (tmpDataExists.value) {
    await api.put('/user/tmp/', tmpData.value).then((res) => {
      notify.success(t('form.updated'));
    });
  } else {
    await api.post('/user/tmp/', tmpData.value).then((res) => {
      notify.success(t('form.saved'));
      tmpDataExists.value = true;
    });
  }
}
</script>
