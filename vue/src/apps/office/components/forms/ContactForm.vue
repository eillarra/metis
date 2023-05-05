<template>
  <dialog-form icon="portrait" :title="obj?.user.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink>
        <q-tab name="info" label="info"></q-tab>
        <q-tab name="remarks" :label="$t('remark', 9)"></q-tab>
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab">
        <q-tab-panel name="info" class="q-pa-md">
          <div v-if="obj" class="q-gutter-md">
            <q-toggle v-model="obj.is_mentor" label="I accept the license and terms" />
            <q-toggle v-model="obj.is_staff" label="I accept the license and terms" />
          </div>
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

const props = defineProps<{
  obj: Contact;
}>();

const tab = ref('info');
const obj = ref<Contact>(props.obj);
</script>
