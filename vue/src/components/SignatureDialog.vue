<template>
  <q-dialog v-model="dialogVisible" @hide="emit('update:modelValue', dialogVisible)">
    <q-layout view="hHh lpR fFf" container class="bg-white metis__dialog-editor" style="height: 600px">
      <q-header class="bg-white q-pt-sm">
        <q-toolbar class="text-primary q-pl-lg q-pr-sm use-default-q-btn">
          <q-icon :name="iconSignature" />
          <q-toolbar-title>{{ title }}</q-toolbar-title>
          <q-space />
          <q-btn flat round v-close-popup :icon="iconClose" />
        </q-toolbar>
      </q-header>
      <q-page-container>
        <markdown-toast-viewer v-model="finalText" :source-text="textToSign" class="q-px-lg" />
      </q-page-container>
      <q-footer class="bg-white text-dark q-pa-lg">
        <q-list class="q-my-md">
          <q-item tag="label" v-ripple>
            <q-item-section avatar top>
              <q-checkbox v-model="acceptanceChecked" />
            </q-item-section>
            <q-item-section v-if="locale == 'en'">
              <q-item-label>Read and approved</q-item-label>
              <q-item-label class="text-body2">
                Signature - by checking 'Read and approved' and clicking the 'sign' button you sign this document and
                expressly acknowledge that it has the same legal value and is legally binding in the same way as an
                originally signed version.
              </q-item-label>
            </q-item-section>
            <q-item-section v-else>
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
          <q-btn @click="signText" unelevated color="ugent" :label="$t('form.sign')" :disable="!acceptanceChecked" />
        </div>
      </q-footer>
    </q-layout>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import MarkdownToastViewer from '@/components/forms/MarkdownToastViewer.vue';

import { iconClose, iconSignature } from '@/icons';

const emit = defineEmits(['update:modelValue']);

const { locale } = useI18n();

const props = defineProps<{
  modelValue: boolean;
  title: string;
  textToSign: string;
  callback: () => void;
}>();

const acceptanceChecked = ref(false);
const finalText = ref<string>('');
const dialogVisible = ref<boolean>(props.modelValue);

const signText = () => {
  props.callback();
  dialogVisible.value = false;
};

watch(
  () => props.modelValue,
  (val) => {
    dialogVisible.value = val;
  }
);
</script>
