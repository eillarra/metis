<template>
  <full-dialog icon="calendar_month" :title="internshipName">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship') }}</q-item-label>
        <q-item clickable @click="tab = 'info'" :active="tab == 'info'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="info_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Info</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'mentors'" :active="tab == 'mentors'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="people_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('mentor', 9) }}</q-item-section>
        </q-item>
        <q-item :disabled="true" :active="tab == 'timesheets'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="schedule" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('timesheet', 9) }}</q-item-section>
        </q-item>
        <q-item :disabled="true" :active="tab == 'evaluations'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="checklist" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('evaluation') }}</q-item-section>
        </q-item>
      </q-list>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-pb-lg">
        <q-tab-panel name="info"> INFO </q-tab-panel>
        <q-tab-panel name="mentors">
          <mentors-view :editable="userIsAdmin" :obj="obj" @update:obj="(obj: Internship) => updateObj(obj)" />
        </q-tab-panel>
      </q-tab-panels>
    </template>
    <template #footer> </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import MentorsView from '@/components/stages/MentorsView.vue';

const props = defineProps<{
  obj: Internship;
}>();

const store = useStore();

const { userIsAdmin } = storeToRefs(store);

const obj = ref<Internship>(props.obj);
const tab = ref<string>('info');
const internshipName = computed<string>(
  () => `${obj.value.Student?.User?.name} - ${obj.value.Place?.name} (${obj.value.Discipline?.name})`
);

function updateObj(obj: Internship) {
  store.updateObj('internship', obj);
}
</script>
