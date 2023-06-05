<template>
  <dialog-form icon="calendar_month" :title="obj.Track?.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="program" :label="$t('program')" icon="commit" />
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
            <readonly-field :label="$t('project')" :value="projectName" />
            <readonly-field :label="$t('student')" :value="obj.Student?.User?.name || '-'" />
            <period-select v-model="obj.period" :periods="filteredPeriods" :label="$t('period')" />
            <discipline-select
              v-if="education"
              v-model="obj.discipline"
              :disciplines="education.disciplines"
              :label="$t('discipline')"
            />
            <div class="row q-col-gutter-lg q-pt-sm q-pl-sm">
              <date-select
                v-model="obj.custom_start_date"
                :label="$t('field.start_date')"
                clearable
                class="col-12 col-md"
              />
              <date-select
                v-model="obj.custom_end_date"
                :label="$t('field.end_date')"
                clearable
                class="col-12 col-md"
              />
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
        <q-btn @click="deleteInternship" unelevated outline color="red" :label="$t('form.internship.delete')" />
        <q-btn
          v-if="obj.student"
          @click="deleteStudent"
          unelevated
          outline
          color="red"
          :label="$t('form.student.delete')"
        />
        <q-space />
        <q-btn @click="save" unelevated color="ugent" :label="$t('form.internship.save')" />
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

import DateSelect from '@/components/forms/DateSelect.vue';
import DialogForm from '@/components/forms/DialogForm.vue';
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import UpdatedByView from '@/components/forms/UpdatedByView.vue';
import RemarksView from '@/components/rel/RemarksView.vue';
import PeriodSelect from '../../components/PeriodSelect.vue';

const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: Internship;
}>();

const { t } = useI18n();
const store = useStore();
const { education, project } = storeToRefs(store);

const obj = ref<Internship>(props.obj);
const tab = ref<string>('info');
const projectName = computed<string>(() => (project.value ? project.value.name : ''));

const filteredPeriods = computed(() => {
  if (!project.value) return [];
  if (!obj.value.Student?.Track) return (project.value as Project).periods;

  return (project.value as Project).periods.filter((period) => {
    return (
      obj.value.Student?.block == period.ProgramInternship?.block &&
      obj.value.Student?.Track?.program_internships.includes(period.program_internship)
    );
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
      student: obj.value.Student?.id,
      track: obj.value.Track?.id,
    })
    .then((res) => {
      obj.value.updated_at = res.data.updated_at;
      obj.value.updated_by = res.data.updated_by;
      store.updateObj('projectInternship', obj.value);
      notify.success(t('form.internship.saved'));
    });
}

function deleteInternship() {
  confirm(t('form.internship.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      store.deleteObj('projectInternship', obj.value);
      notify.success(t('form.internship.deleted'));
      emit('delete:obj');
    });
  });
}

function deleteStudent() {
  confirm(t('form.internship.confirm_delete_student'), () => {
    api.patch(obj.value.self, { student: null }).then(() => {
      obj.value.student = null;
      obj.value.Student = undefined;
      store.updateObj('projectInternship', obj.value);
      notify.success(t('form.internship.deleted_student'));
    });
  });
}
</script>
