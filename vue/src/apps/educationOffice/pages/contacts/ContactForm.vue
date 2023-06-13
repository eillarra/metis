<template>
  <dialog-form icon="portrait" :title="obj.user.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="remarks" :label="$t('remark', 9)" icon="chat_bubble_outline" />
      </q-tabs>
      <q-space />
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="updated_by" icon="history_toggle_off" class="q-px-none" />
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-px-sm">
        <q-tab-panel name="info">
          <div class="q-gutter-sm">
            <readonly-field v-if="obj.Place" :label="$t('place')" :value="obj.Place?.name" />
            <div class="row q-col-gutter-lg q-pt-sm">
              <q-checkbox v-model="obj.is_mentor" :label="t('mentor')" class="col-6 col-md-2" />
              <q-checkbox
                v-if="education?.configuration?.place_contact_is_staff"
                v-model="obj.is_staff"
                :label="t('staff')"
                class="col-6 col-md-2"
              />
              <q-checkbox v-model="obj.is_admin" :label="t('admin')" class="col-6 col-md-2" />
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoints="remarkEndpoints" />
        </q-tab-panel>
        <q-tab-panel name="updated_by">
          <updated-by-view :obj="obj" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <div v-if="tab == 'info'" class="flex q-gutter-sm q-pa-lg">
        <q-btn @click="removeContact" outline color="red" :label="$t('form.contact.delete')" />
        <q-space />
        <q-btn @click="inviteContact" outline color="ugent" :label="$t('form.invite')" />
        <q-btn @click="save" unelevated color="ugent" :label="$t('form.contact.save')" />
      </div>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import DialogForm from '@/components/forms/DialogForm.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import UpdatedByView from '@/components/forms/UpdatedByView.vue';
import RemarksView from '@/components/rel/RemarksView.vue';

const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: Contact;
}>();

const { t } = useI18n();
const store = useStore();
const { education } = storeToRefs(store);

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
    .then((res) => {
      obj.value.updated_at = res.data.updated_at;
      obj.value.updated_by = res.data.updated_by;
      store.updateObj('contact', obj.value);
      notify.success('Contact info saved');
    });
}

function removeContact() {
  confirm(t('form.contact.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      store.deleteObj('contact', obj.value);
      notify.success(t('form.contact.deleted'));
      emit('delete:obj');
    });
  });
}

function inviteContact() {
  api.post(`${obj.value.self}invite/`).then(() => {
    notify.success(t('form.contact.create.invited'));
  });
}
</script>
