<template>
  <dialog-form icon="person" :title="studentUser.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="internships" :label="$t('internship', 9)" />
        <q-tab name="addresses" :label="$t('address', 9)" icon="map" />
        <q-tab name="remarks" :label="remarkCount" icon="chat_bubble_outline" />
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-px-sm">
        <q-tab-panel name="info">
          <div class="q-gutter-xs">
            <div class="row q-col-gutter-lg q-pl-xs">
              <readonly-field
                v-if="obj.Project"
                :label="$t('project')"
                :value="obj.Project?.name"
                class="col-12 col-md"
              />
              <readonly-field :label="$t('track')" :value="obj.Track?.name || '-'" class="col-12 col-md" />
              <readonly-field :label="$t('program_block')" :value="obj.Block?.name" class="col-12 col-md" />
            </div>
            <readonly-field :label="$t('student')" :value="studentUser.name" />
            <readonly-field :label="$t('field.email')" :value="studentUser.email" />
          </div>
        </q-tab-panel>
        <q-tab-panel name="internships"> - TODO: Show internship info </q-tab-panel>
        <q-tab-panel name="addresses">
          <address-cards :api-endpoint="studentUser.rel_addresses" in-dialog />
        </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoints="remarkEndpoints" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <div v-if="tab == 'info'" class="flex q-gutter-sm q-pa-lg">
        <q-btn
          @click="deleteStudent"
          outline
          color="red"
          :label="$t('form.student.delete')"
          :disable="projectStudentsWithInternships.has(obj.id)"
        />
        <q-space />
        <q-btn
          v-if="!obj.is_active"
          @click="makeActive(true)"
          unelevated
          color="ugent"
          :label="$t('form.student.make_active')"
        />
        <q-btn v-else @click="makeActive(false)" outline color="ugent" :label="$t('form.student.make_not_active')" />
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
import AddressCards from '@/components/rel/AddressCards.vue';
import RemarksView from '@/components/rel/RemarksView.vue';

const { t } = useI18n();
const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: StudentUser;
}>();

const store = useStore();
const { project, projectStudentsWithInternships } = storeToRefs(store);

const studentUser = ref<StudentUser>(props.obj);
const obj = ref<Student>(props.obj.student_set.find((obj) => obj.project == project.value?.id) as Student);
const tab = ref<string>('info');

const remarkCount = computed<number>(() => {
  if (!props.obj) return 0;
  return props.obj.student_set.reduce((acc, projectStudent: Student) => {
    return acc + projectStudent.remark_count;
  }, 0);
});

const remarkEndpoints = computed<null | Record<string, ApiEndpoint>>(() => {
  if (!props.obj) return null;

  let acc: Record<string, ApiEndpoint> = {};
  return props.obj.student_set.reduce((acc, projectStudent: Student) => {
    acc[(projectStudent.Project as Project).name] = projectStudent.rel_remarks;
    return acc;
  }, acc);
});

function makeActive(active: boolean) {
  api
    .patch(obj.value.self, {
      is_active: active,
    })
    .then(() => {
      notify.success(t('form.student.saved'));
      obj.value.is_active = active;
      store.updateObj('student', obj.value);
    });
}

function deleteStudent() {
  confirm(t('form.student.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      // we remove the whole student/user from the store, because the student is deleted from the project
      // when we change projects, the student might be loaded again for the other project
      store.deleteObj('student', studentUser.value);
      notify.success(t('form.student.deleted'));
      emit('delete:obj');
    });
  });
}
</script>
