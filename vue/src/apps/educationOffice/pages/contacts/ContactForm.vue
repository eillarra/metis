<template>
  <dialog-form :icon="iconContact" :title="obj.user.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" :icon="iconInfo" />
        <q-tab name="remarks" :label="$t('remark', 9)" :icon="iconChat" />
      </q-tabs>
      <q-space />
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="updated_by" :icon="iconTimeDashed" class="q-px-none" />
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
            <div class="q-mt-md">
              <span class="text-body2">{{ $t('field.email_address', 9) }}</span>
              <readonly-field v-for="eaddress in sortedEmailAddresses" :key="eaddress.email" :value="eaddress.email">
                <template #prepend>
                  <q-icon v-if="eaddress.primary" :name="iconStar" color="dark" size="xs" />
                  <q-icon
                    v-else
                    @click="changeContactPrimaryEmail(eaddress.email)"
                    :name="iconStarEmpty"
                    color="dark"
                    size="xs"
                    class="cursor-pointer"
                  />
                </template>
                <template #append>
                  <q-icon
                    v-if="!eaddress.primary"
                    @click="deleteContactEmail(eaddress.email)"
                    color="red"
                    :name="iconDelete"
                    size="xs"
                    class="cursor-pointer"
                  />
                </template>
              </readonly-field>
              <q-input
                :placeholder="'Add new email'"
                v-model.trim="newEmail"
                type="email"
                dense
                class="use-default-q-btn"
              >
                <template #append>
                  <q-icon @click="addContactEmail" :name="iconAddBox" color="ugent" size="xs" class="cursor-pointer" />
                </template>
              </q-input>
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
        <q-btn @click="welcomeContact" outline color="ugent" :label="$t('form.send_welcome_email')" />
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

import {
  iconAddBox,
  iconChat,
  iconContact,
  iconDelete,
  iconInfo,
  iconStar,
  iconStarEmpty,
  iconTimeDashed,
} from '@/icons';

const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: Contact;
}>();

const { t } = useI18n();
const store = useStore();
const { education, project } = storeToRefs(store);

const tab = ref<string>('info');
const obj = ref<Contact>(props.obj);
const newEmail = ref<string>('');

const sortedEmailAddresses = computed<EmailAddressObject[]>(() => {
  return obj.value.email_addresses.sort((a, b) => {
    if (a.primary && !b.primary) return -1;
    if (!a.primary && b.primary) return 1;
    return a.email.localeCompare(b.email);
  });
});

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
  confirm(t('form.contact.confirm_delete', { name: obj.value.user.name }), () => {
    api.delete(obj.value.self).then(() => {
      store.deleteObj('contact', obj.value);
      notify.success(t('form.contact.deleted'));
      emit('delete:obj');
    });
  });
}

function welcomeContact() {
  const data = {
    project_id: project.value?.id || null,
  };

  api.post(`${obj.value.self}invite/`, data).then(() => {
    notify.success(t('form.contact.create.welcome_email_sent'));
  });
}

function addContactEmail() {
  if (!newEmail.value) return;

  api
    .post(`${obj.value.self}add_email/`, {
      email: newEmail.value,
    })
    .then((res) => {
      obj.value.email_addresses = res.data.email_addresses;
      newEmail.value = '';
      notify.success(t('form.contact.email.added'));
    });
}

function deleteContactEmail(email: string) {
  confirm(t('form.contact.email.confirm_delete', { email: email }), () => {
    api
      .post(`${obj.value.self}delete_email/`, {
        email: email,
      })
      .then(() => {
        obj.value.email_addresses = obj.value.email_addresses.filter((e) => e.email !== email);
        notify.success(t('form.contact.email.deleted'));
      });
  });
}

function changeContactPrimaryEmail(email: string) {
  confirm(t('form.contact.email.confirm_change_primary', { email: email, name: obj.value.user.name }), () => {
    api
      .post(`${obj.value.self}change_primary_email/`, {
        email: email,
      })
      .then((res) => {
        obj.value.email_addresses = res.data.email_addresses;
        notify.success(t('form.contact.email.changed_primary'));
      });
  });
}
</script>
