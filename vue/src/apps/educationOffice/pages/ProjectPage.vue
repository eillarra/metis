<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('project') }}</h3>
    <div class="col"></div>
  </div>
  <div>
    <div class="flex">
      <q-tabs v-model="tab" dense shrink inline-label no-caps align="left">
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="texts" :label="$t('text', 9)" icon="notes" />
      </q-tabs>
      <q-space />
      <q-tabs v-if="project" v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="updated_by" icon="history_toggle_off" class="q-px-none" />
      </q-tabs>
    </div>
    <q-tab-panels v-model="tab">
      <q-tab-panel name="info" class="q-px-none"> - </q-tab-panel>
      <q-tab-panel name="texts" class="q-px-none">
        <texts-view :api-endpoint="textsEndpoint" :text-types="education?.configuration?.project_text_types" />
      </q-tab-panel>
      <q-tab-panel name="updated_by" class="q-px-none">
        <updated-by-view v-if="project" :obj="project" />
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../store';

import UpdatedByView from '@/components/forms/UpdatedByView.vue';
import TextsView from '@/components/rel/TextsView.vue';

const { education, project } = storeToRefs(useStore());
const tab = ref<string>('texts');

const textsEndpoint = computed<null | ApiEndpoint>(() => {
  if (!project.value) return null;
  return project.value.rel_texts;
});
</script>
