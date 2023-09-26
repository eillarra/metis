<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('document', 9) }}</h3>
    <div class="col"></div>
  </div>
  <div v-if="signatures">
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

import SignaturesTable from './SignaturesTable.vue';

const page = usePage();

const { signatures } = storeToRefs(useStore());

const requiredTexts = computed<TextEntry[]>(() => page.props.required_texts as TextEntry[]);
</script>
