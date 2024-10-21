<template>
  <files-read-only-view :files="files">
    <template #title>
      <h3 class="text-ugent col-12 col-md-3 q-mb-lg">{{ $t('document', 9) }}</h3>
    </template>
  </files-read-only-view>
  <div v-if="signatures" class="q-mt-xl">
    <signatures-table v-if="signatures.length" :signatures="signatures" :texts="requiredTexts" />
    <div v-else class="col-12 col-md-3">
      <p>{{ $t('signatures.no_results') }}</p>
      <p class="text-grey-4 text-h2 text-mono q-mt-xl">(^-^*)</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { usePage } from '@inertiajs/vue3';

import { useStore } from '../../store.js';

import FilesReadOnlyView from '@/components/rel/FilesReadOnlyView.vue';
import SignaturesTable from './SignaturesTable.vue';

const page = usePage();

const { signatures } = storeToRefs(useStore());

const requiredTexts = computed<TextEntry[]>(() => page.props.required_texts as TextEntry[]);

const files = computed<RelatedFile[]>(() => page.props.files as RelatedFile[]);
</script>
