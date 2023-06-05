<style lang="scss">
.metis__dialog-editor {
  .q-dialog__inner--minimized > & {
    width: 900px !important;
    max-width: 100vw;
  }
}
</style>

<template>
  <div v-if="loading" class="flex flex-center q-mt-xl">
    <q-spinner color="grey-3" size="4em" />
  </div>
  <div v-else>
    <div v-show="pendingTexts.length" class="q-gutter-sm q-mb-md">
      <q-banner
        v-for="textType in pendingTexts"
        :key="textType.code"
        inline-actions
        class="bg-blue-1 cursor-pointer"
        @click="addText(textType)"
      >
        <template #default>
          <span class="text-body1"
            ><q-icon name="post_add" class="q-mr-sm" />{{
              locale === 'en' ? textType.title.en : textType.title.nl
            }}</span
          >
        </template>
        <template #action>
          <q-btn unelevated flat color="ugent" :label="$t('form.add')" no-caps></q-btn>
        </template>
      </q-banner>
    </div>
    <div class="row q-col-gutter-sm q-mt-none">
      <div
        v-for="textEntry in texts"
        :key="textEntry.id"
        flat
        bordered
        class="col-4 col-md-2 align-items-stretch"
        :class="{ 'col-md-4': container }"
      >
        <q-card flat bordered class="column full-height">
          <q-card-section>
            <div v-if="locale == 'en'" class="text-h6">{{ textEntry.title_en }}</div>
            <div v-else class="text-h6">{{ textEntry.title_nl }}</div>
            <q-skeleton type="text" animation="none" class="q-mt-md" />
            <q-skeleton type="text" animation="none" width="60%" />
          </q-card-section>
          <q-space />
          <q-card-actions class="use-default-q-btn">
            <q-space />
            <q-btn
              square
              unelevated
              icon="edit"
              @click="obj = textEntry as TextEntry"
              color="ugent"
              no-caps
              size="sm"
              class="q-mb-sm q-mr-sm"
            />
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </div>
  <q-dialog v-model="dialogVisible">
    <q-layout v-if="obj" view="hHh lpR fFf" container class="bg-white metis__dialog-editor" style="height: 600px">
      <q-header class="bg-white q-pt-sm">
        <q-toolbar class="text-primary q-pl-lg q-pr-sm">
          <q-icon name="notes" />
          <q-toolbar-title v-if="selectedTextType">{{
            locale === 'en' ? selectedTextType.title.en : selectedTextType.title.nl
          }}</q-toolbar-title>
          <q-space />
          <q-btn flat dense v-close-popup icon="close" style="padding: 8px" />
        </q-toolbar>
        <q-toolbar class="text-dark text-body1 q-px-lg" style="min-height: auto">
          <q-tabs v-model="tab" dense shrink inline-label no-caps>
            <q-tab name="nl" label="Nederlands" icon="translate" />
            <q-tab name="en" label="English" icon="translate" />
          </q-tabs>
          <q-space />
          <q-tabs v-if="obj.id" v-model="tab" dense shrink inline-label no-caps>
            <q-tab name="updated_by" icon="history_toggle_off" class="q-px-none" />
          </q-tabs>
        </q-toolbar>
      </q-header>
      <q-page-container>
        <q-page>
          <q-tab-panels v-model="tab" class="q-px-sm">
            <q-tab-panel name="nl">
              <q-input v-model="obj.title_nl" dense :label="$t('field.title')" class="q-mb-md col-12 col-md-8" />
              <markdown-toast-editor v-model="obj.text_nl" />
            </q-tab-panel>
            <q-tab-panel name="en">
              <q-input v-model="obj.title_en" dense :label="$t('field.title')" class="q-mb-md col-12 col-md-8" />
              <markdown-toast-editor v-model="obj.text_en" />
            </q-tab-panel>
            <q-tab-panel name="updated_by">
              <updated-by-view :obj="obj" />
            </q-tab-panel>
          </q-tab-panels>
        </q-page>
      </q-page-container>
      <q-footer class="bg-white">
        <div class="flex q-gutter-sm q-pa-lg">
          <q-btn
            @click="deleteText"
            unelevated
            outline
            color="red"
            :label="$t('form.text_entry.delete')"
            :disable="!obj.id"
          />
          <q-space />
          <q-btn
            v-if="obj.id"
            @click="updateText"
            unelevated
            color="ugent"
            :label="$t('form.text_entry.save')"
            :disable="!obj.title_en || !obj.title_nl || !obj.text_en || !obj.text_nl"
          />
          <q-btn
            v-else
            @click="createText"
            unelevated
            color="ugent"
            :label="$t('form.text_entry.save')"
            :disable="!obj.title_en || !obj.title_nl || !obj.text_en || !obj.text_nl"
          />
        </div>
      </q-footer>
    </q-layout>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';

import MarkdownToastEditor from '@/components/forms/MarkdownToastEditor.vue';
import UpdatedByView from '@/components/forms/UpdatedByView.vue';

const { t, locale } = useI18n();

const props = defineProps<{
  apiEndpoint: ApiEndpoint | null;
  textTypes: TextEntryType[];
  container?: boolean;
}>();

const tab = ref<string>('nl');
const obj = ref<TextEntry | null>(null);
const loading = ref<boolean>(true);
const texts = ref<TextEntry[]>([]);

const selectedTextType = computed<TextEntryType | null>(() => {
  if (!obj.value) return null;
  return props.textTypes.find((c) => c.code === (obj.value as TextEntry).code) || null;
});

const dialogVisible = computed<boolean>({
  get() {
    return !!obj.value;
  },
  set(value) {
    if (!value) {
      obj.value = null;
    }
  },
});

const pendingTexts = computed<TextEntryType[]>(() => {
  if (!texts.value || !props.textTypes?.length) return [];
  // check what content types are not yet in the texts, via code
  return props.textTypes.filter((c) => !texts.value.find((d) => d.code === c.code));
});

async function fetchTexts() {
  if (!props.apiEndpoint) return;
  await api.get<TextEntry[]>(props.apiEndpoint).then((res) => {
    texts.value = res.data.sort((a, b) => a.code.localeCompare(b.code));
    loading.value = false;
  });
}

async function addText(textType: TextEntryType) {
  obj.value = <TextEntry>{
    code: textType.code,
    title_en: textType.title['en'],
    title_nl: textType.title['nl'],
    text_en: '',
    text_nl: '',
  };
}

async function createText() {
  if (!props.apiEndpoint || !obj.value) return;
  await api.post(props.apiEndpoint, obj.value).then((res) => {
    texts.value.push(res.data);
    notify.success(t('form.text_entry.create.success'));
    obj.value = null;
  });
}

async function updateText() {
  if (!obj.value) return;
  api.put((obj.value as TextEntry).self, obj.value).then((res) => {
    const idx = texts.value.findIndex((c) => c.id === (obj.value as TextEntry).id);
    texts.value.splice(idx, 1, res.data);
    notify.success(t('form.text_entry.update.saved'));
    obj.value = null;
  });
}

async function deleteText() {
  if (!obj.value) return;
  confirm(t('form.text_entry.confirm_delete'), () => {
    api.delete((obj.value as TextEntry).self).then(() => {
      texts.value.splice(texts.value.indexOf(obj.value as TextEntry), 1);
      notify.success(t('form.text_entry.deleted'));
      obj.value = null;
    });
  });
}

fetchTexts();

watch(() => props.apiEndpoint, fetchTexts);
</script>
