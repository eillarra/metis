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
          :icon="iconAdd"
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
          <template #badges>
            <visibility-badges :tags="file.tags" />
          </template>
          <template #actions>
            <q-btn flat round :href="file.url" target="_blank" :icon="iconDownload" :size="btnSize" />
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
      <dialog-form small :icon="iconAdd" :title="$t('file')">
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
                  <q-icon :name="iconAttachment" />
                </template>
              </q-file>
              <q-input v-model="formData.description" :label="$t('field.description')" dense class="col-12" />
              <visibility-options
                v-if="visibilityOptions"
                v-model="formData.tags"
                :options="visibilityOptions"
                class="col-12"
              />
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

import FileCard from '@/components/FileCard.vue';
import NoResults from '@/components/NoResults.vue';
import DialogForm from '@/components/forms/DialogForm.vue';
import VisibilityBadges from '@/components/forms/VisibilityBadges.vue';
import VisibilityOptions from '@/components/forms/VisibilityOptions.vue';

import { iconAdd, iconAttachment, iconDelete, iconDownload } from '@/icons';

const { t } = useI18n();

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  accept?: string;
  customCreateDescription?: string;
  visibilityOptions?: string[];
  readOnly?: boolean;
}>();

const btnSize = '13px';

const loading = ref<boolean>(true);
const dialogVisible = ref<boolean>(false);
const files = ref<RelatedFile[]>([]);
const file = ref<File | null>(null);
const formData = ref({
  description: null as string | null,
  tags: [] as Tags,
});

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
  multipartFormData.append('file', file.value);
  multipartFormData.append('json', JSON.stringify(formData.value));

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

fetchRelatedFiles();

watch(() => props.apiEndpoint, fetchRelatedFiles);

function reset() {
  file.value = null;
  formData.value.description = null;
  formData.value.tags = [];
  dialogVisible.value = false;
}
</script>
