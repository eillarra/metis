<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('signature', 9) }}</h3>
    <div class="col"></div>
  </div>
  <signatures-table v-if="signatures" :signatures="signatures" :texts="requiredTexts" />
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
