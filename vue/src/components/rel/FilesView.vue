<template>
  <div>
    <div class="row q-col-gutter-sm">
      <slot name="title">
        <h4 class="col-12 col-md-3 q-mt-none q-mb-lg">{{ $t('document', 9) }}</h4>
      </slot>
      <q-space />
      <div v-if="!readOnly" class="col-6 col-md-1 ugent__create-btn">
        <q-btn
          unelevated
          color="blue-1"
          :label="$t('form.new')"
          icon="add"
          class="text-ugent full-width"
          @click="dialogVisible = true"
        />
      </div>
    </div>
    <div v-if="loading" class="flex flex-center q-mt-xl">
      <q-spinner color="grey-3" size="4em" />
    </div>
    <no-results v-else-if="!files.length" />
    <div v-else class="row q-col-gutter-sm">
      <div v-for="file in files" :key="file.id" class="col-12 col-sm-4 col-md-2">
        <file-card :title="file.description" class="column full-height">
          <template #actions>
            <q-btn flat round icon="visibility" :size="btnSize" @click="openRelatedFile(file)" />
            <q-space />
            <q-btn
              v-if="!readOnly"
              flat
              round
              :icon="iconDelete"
              :size="btnSize"
              color="red"
              @click="deleteRelatedFile(file)"
            />
          </template>
        </file-card>
      </div>
    </div>
    <q-dialog v-model="dialogVisible">
      <dialog-form small icon="add" :title="$t('file')">
        <template #page>
          <div class="q-pa-lg">
            {{ customCreateDescription }}
            <div class="row q-col-gutter-sm">
              <q-file
                v-model="file"
                :label="$t('file')"
                :accept="accept ? accept : '.pdf'"
                dense
                clearable
                class="col-12"
              >
                <template v-slot:prepend>
                  <q-icon name="attachment" />
                </template>
              </q-file>
              <q-input v-model="formData.description" :label="$t('field.description')" dense class="col-12" />
              <slot name="custom-fields" />
            </div>
          </div>
        </template>
        <template #footer>
          <div class="flex q-gutter-sm q-pa-lg">
            <q-space />
            <q-btn
              unelevated
              @click="addRelatedFile"
              color="ugent"
              :label="$t('form.file.create.new')"
              :disable="!file || !formData.description"
            />
          </div>
        </template>
      </dialog-form>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';

import { iconDelete } from '@/icons';

import FileCard from '@/components/FileCard.vue';
import NoResults from '@/components/NoResults.vue';
import DialogForm from '@/components/forms/DialogForm.vue';

const { t } = useI18n();

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  accept?: string;
  customCreateDescription?: string;
  customFieldsProcessor?: (formData: Record<string, any>) => Record<string, any>;
  readOnly?: boolean;
}>();

const btnSize = '13px';

const loading = ref<boolean>(true);
const dialogVisible = ref<boolean>(false);
const files = ref<RelatedFile[]>([]);
const file = ref<File | null>(null);
const formData = ref({
  description: null as string | null,
});

const customFieldsProcessor = props.customFieldsProcessor || ((formData: Record<string, any>) => formData);

async function fetchRelatedFiles() {
  if (!props.apiEndpoint) return;
  await api.get<RelatedFile[]>(props.apiEndpoint).then((res) => {
    files.value = res.data.sort((a, b) => a.description.localeCompare(b.description));
    loading.value = false;
  });
}

async function addRelatedFile() {
  if (!props.apiEndpoint || !formData.value.description || !file.value) return;

  const multipartFormData = new FormData();
  multipartFormData.append('description', formData.value.description);
  multipartFormData.append('file', file.value);

  api
    .post<RelatedFile>(props.apiEndpoint, multipartFormData, {
      headers: {
        'Content-Disposition': 'attachment; filename=' + file.value.name,
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((res) => {
      notify.success(t('form.file.create.success'));
      files.value.push(res.data);
      reset();
    });
}

async function deleteRelatedFile(file: RelatedFile) {
  confirm(t('form.file.confirm_delete'), () => {
    api.delete(file.self).then(() => {
      notify.success(t('form.file.deleted'));
      files.value.splice(files.value.indexOf(file), 1);
    });
  });
}

async function openRelatedFile(file: RelatedFile) {
  window.open(file.url, '_blank');
}

fetchRelatedFiles();

watch(() => props.apiEndpoint, fetchRelatedFiles);

function reset() {
  file.value = null;
  formData.value.description = null;
  dialogVisible.value = false;
}
</script>
