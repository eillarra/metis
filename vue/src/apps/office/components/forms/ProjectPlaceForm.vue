<template>
  <dialog-form icon="business" :title="obj.place.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="contacts" :label="$t('contact', 9)" icon="portrait" />
        <q-tab name="contents" :label="$t('text', 9)" icon="notes" />
        <q-tab name="remarks" :label="`${$t('remark', 9)} (${remarkCount})`" icon="chat_bubble_outline" />
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-px-sm">
        <q-tab-panel name="info">
          <div class="q-gutter-sm">
            <q-input v-model="projectName" dense :label="$t('project')" readonly />
            <q-input v-model="obj.place.name" dense :label="$t('field.name')" />
            <q-input v-model="obj.place.code" dense :label="$t('field.code')" />
            <discipline-select
              v-if="education"
              v-model="obj.disciplines"
              multiple
              :disciplines="education.disciplines"
              :label="$t('discipline', 9)"
            />
          </div>
        </q-tab-panel>
        <q-tab-panel name="contacts">
          <q-list class="q-pa-none">
            <q-item v-for="contact in obj.place.contacts" :key="contact.id">
              <q-item-section>
                <q-item-label>{{ contact.user.name }}</q-item-label>
                <q-item-label caption>{{ contact.user.email }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn flat icon="delete" @click="deleteContact(contact)" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>
        <q-tab-panel name="contents">
          <contents-view />
        </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoints="remarkEndpoints" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <div v-if="tab == 'info'" class="flex q-gutter-sm q-pa-lg">
        <q-btn
          @click="deletePlace"
          unelevated
          outline
          color="red"
          :label="$t('form.place.delete')"
          :disable="projectPlacesWithInternships.has(obj.id)"
        />
        <q-space />
        <q-btn @click="save" unelevated color="primary" :label="$t('form.place.save')" />
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

import { useOfficeStore } from '../../store';

import DialogForm from '@/components/forms/DialogForm.vue';
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';
import ContentsView from '@/components/rel/ContentsView.vue';
import RemarksView from '@/components/rel/RemarksView.vue';

const { t } = useI18n();
const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: ProjectPlace;
}>();

const officeStore = useOfficeStore();
const { education, project, projectPlacesWithInternships } = storeToRefs(officeStore);

const obj = ref<ProjectPlace>(props.obj);
const tab = ref<string>('info');
const projectName = computed<string>(() => (project.value ? project.value.name : ''));

const remarkCount = computed<number>(() => {
  if (!props.obj) return 0;
  return props.obj.place.remark_count + props.obj.remark_count;
});

const remarkEndpoints = computed<null | Record<string, ApiEndpoint>>(() => {
  if (!props.obj) return null;

  return {
    default: props.obj.place.rel_remarks,
    // place: props.obj.place.rel_remarks,
    // projectPlace: props.obj.rel_remarks, // we only add remarks at Education level, for now
  };
});

function save() {
  api
    .put(obj.value.place.self, {
      ...obj.value.place,
    })
    .then(() => {
      api
        .put(obj.value.self, {
          ...obj.value,
          discipline_ids: obj.value.disciplines.map((d) => d.id),
          place_id: obj.value.place.id,
        })
        .then(() => {
          officeStore.updateObj('projectPlace', obj.value);
          notify.success(t('form.place.saved'));
        });
    });
}

function deletePlace() {
  confirm(t('form.student.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      officeStore.deleteObj('projectPlace', obj.value);
      notify.success(t('form.place.deleted'));
      emit('delete:obj');
    });
  });
}

function deleteContact(contact: Contact) {
  confirm(t('form.contact.confirm_delete'), () => {
    api.delete(contact.self).then(() => {
      obj.value.place.contacts = obj.value.place.contacts.filter((c) => c.id !== contact.id);
      officeStore.updateObj('projectPlace', obj.value);
      notify.success(t('form.contact.deleted'));
    });
  });
}
</script>
