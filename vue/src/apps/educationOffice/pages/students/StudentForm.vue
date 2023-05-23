<template>
  <dialog-form icon="person" :title="student.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="internships" :label="$t('internship', 9)" />
        <q-tab name="remarks" :label="`${$t('remark', 9)} (${remarkCount})`" icon="chat_bubble_outline" />
      </q-tabs>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-px-sm">
        <q-tab-panel name="info">
          <div class="q-gutter-xs">
            <div class="row q-col-gutter-lg q-pl-xs">
              <q-input v-model="obj.project.name" dense :label="$t('project')" readonly class="col-12 col-md" />
              <q-input v-model="obj.block.name" dense :label="$t('program_block')" readonly class="col-12 col-md" />
            </div>
            <q-input v-model="student.name" dense :label="$t('student')" readonly />
            <q-input v-model="student.email" dense :label="$t('field.email')" readonly />
          </div>
        </q-tab-panel>
        <q-tab-panel name="internships"> - TODO: Show internship info </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoints="remarkEndpoints" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer>
      <div v-if="tab == 'info'" class="flex q-gutter-sm q-pa-lg">
        <q-btn
          @click="deleteStudent"
          unelevated
          outline
          color="red"
          :label="$t('form.student.delete')"
          :disable="projectStudentsWithInternships.has(obj.id)"
        />
        <q-space />
        <!--<q-btn @click="save" unelevated color="ugent" :label="$t('form.student.save')" />-->
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
import RemarksView from '@/components/rel/RemarksView.vue';

const { t } = useI18n();
const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: Student;
}>();

const officeStore = useStore();
const { project, projectStudentsWithInternships } = storeToRefs(officeStore);

const student = ref<Student>(props.obj);
const obj = ref<ProjectStudent>(
  props.obj.student_set.find((obj) => obj.project.id == project.value?.id) as ProjectStudent
);
const tab = ref<string>('info');

const remarkCount = computed<number>(() => {
  if (!props.obj) return 0;
  return props.obj.student_set.reduce((acc, projectStudent: ProjectStudent) => {
    return acc + projectStudent.remark_count;
  }, 0);
});

const remarkEndpoints = computed<null | Record<string, ApiEndpoint>>(() => {
  if (!props.obj) return null;

  let acc: Record<string, ApiEndpoint> = {};
  return props.obj.student_set.reduce((acc, projectStudent: ProjectStudent) => {
    acc[projectStudent.project.name] = projectStudent.rel_remarks;
    return acc;
  }, acc);
});

function deleteStudent() {
  confirm(t('form.student.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      // we remove the whole student/user from the store, because the student is deleted from the project
      // when we change projects, the student might be loaded again for the other project
      officeStore.deleteObj('student', student.value);
      notify.success(t('form.student.deleted'));
      emit('delete:obj');
    });
  });
}
</script>
