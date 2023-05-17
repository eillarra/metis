<template>
  <dialog-form icon="portrait" :title="obj.user.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="remarks" :label="$t('remark', 9)" icon="chat_bubble_outline" />
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab">
        <q-tab-panel name="info" class="q-pa-md">
          <div class="q-gutter-sm">
            <q-toggle v-model="obj.is_mentor" label="mentor" />
            <q-toggle v-model="obj.is_staff" label="staff" />
          </div>
        </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoints="remarkEndpoints" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <div v-if="tab == 'info'" class="flex q-gutter-sm q-pa-lg">
        <q-btn @click="removeContact" unelevated outline color="red" :label="$t('form.contact.delete')" />
        <q-space />
        <q-btn @click="save" unelevated color="primary" :label="$t('form.contact.save')" />
      </div>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';

import { useOfficeStore } from '../../store';

import DialogForm from '@/components/forms/DialogForm.vue';
import RemarksView from '@/components/rel/RemarksView.vue';

const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: Contact;
}>();

const { t } = useI18n();
const officeStore = useOfficeStore();

const tab = ref<string>('info');
const obj = ref<Contact>(props.obj);

const remarkEndpoints = computed<null | Record<string, ApiEndpoint>>(() => {
  if (!props.obj) return null;
  return {
    default: props.obj.rel_remarks,
  };
});

function save() {
  api
    .put(obj.value.self, {
      ...obj.value,
      user_id: obj.value.user.id,
    })
    .then(() => {
      officeStore.updateObj('contact', obj.value);
      notify.success('Contact info saved');
    });
}

function removeContact() {
  confirm(t('form.contact.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      officeStore.deleteObj('contact', obj.value);
      notify.success(t('form.contact.deleted'));
      emit('delete:obj');
    });
  });
}
</script>
