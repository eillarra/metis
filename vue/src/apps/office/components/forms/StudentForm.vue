<template>
  <dialog-form icon="person" :title="obj?.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink>
        <q-tab name="info" label="info"></q-tab>
        <q-tab name="remarks" :label="$t('remark', 9)"></q-tab>
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab">
        <q-tab-panel name="info" class="q-pa-md">
          {{ obj }}
        </q-tab-panel>
        <q-tab-panel name="remarks"> remarks </q-tab-panel>
      </q-tab-panels>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import DialogForm from '@/components/forms/DialogForm.vue';

defineProps<{
  obj: Student | null;
}>();

const tab = ref('info');
</script>
