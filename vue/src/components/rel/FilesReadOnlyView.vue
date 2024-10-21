<template>
  <div>
    <div class="row q-col-gutter-sm">
      <slot name="title">
        <h4 class="col-12 col-md-3 q-mt-none q-mb-lg">{{ $t('document', 9) }}</h4>
      </slot>
    </div>
    <no-results v-if="!files.length" />
    <div v-else class="row q-col-gutter-sm">
      <div v-for="file in files" :key="file.id" class="col-12 col-sm-4 col-md-2">
        <file-card :title="file.description" class="column full-height">
          <template #actions>
            <q-btn flat round :icon="iconDownload" :size="btnSize" @click="openRelatedFile(file)" />
          </template>
        </file-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import FileCard from '@/components/FileCard.vue';
import NoResults from '@/components/NoResults.vue';

import { iconDownload } from '@/icons';

defineProps<{
  files: RelatedFile[];
}>();

const btnSize = '13px';

async function openRelatedFile(file: RelatedFile) {
  window.open(file.url, '_blank');
}
</script>
