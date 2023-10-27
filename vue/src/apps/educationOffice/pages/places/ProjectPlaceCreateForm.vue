<template>
  <dialog-form icon="add" :title="$t('place')">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" :title="$t('form.place.create.add_existing')" icon="search" active-icon="search">
          {{ $t('form.place.create.search') }}
          <div class="q-gutter-sm q-mt-sm">
            <api-autocomplete
              v-model="found"
              clearable
              :data-source="(education as Education).rel_places"
              :mapper="placeMapper"
              :label="$t('place')"
            />
            <discipline-select
              v-if="education && found"
              v-model="disciplines"
              multiple
              :disciplines="education.disciplines"
              :label="$t('discipline', 9)"
            />
          </div>
          <q-stepper-navigation class="flex">
            <q-btn
              unelevated
              @click="step = 2"
              color="blue-1"
              text-color="ugent"
              :label="$t('form.skip')"
              :disable="!!found"
            />
            <q-space />
            <q-btn
              unelevated
              @click="addProjectPlace"
              color="ugent"
              :label="$t('form.add_to_project')"
              :disable="!found || !disciplines.length"
            />
          </q-stepper-navigation>
        </q-step>
        <q-step :name="2" :title="$t('form.place.create.new')" icon="add">
          <div class="q-gutter-sm q-mt-sm">
            <q-input v-model="obj.name" dense :label="$t('field.name')" />
            <q-input v-model="obj.code" dense :label="$t('field.code')" />
            <discipline-select
              v-if="education"
              v-model="disciplines"
              multiple
              :disciplines="education.disciplines"
              :label="$t('discipline', 9)"
            />
          </div>
        </q-step>
      </q-stepper>
    </template>
    <template #footer>
      <div v-if="step == 2" class="flex q-gutter-sm q-pa-lg">
        <q-btn unelevated @click="step = 1" color="blue-1" text-color="ugent" :label="$t('form.back')" />
        <q-space />
        <q-btn
          unelevated
          @click="createPlace"
          color="ugent"
          :label="$t('form.add_to_project')"
          :disable="!obj.name || !obj.code || !disciplines.length"
        />
      </div>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import ApiAutocomplete from '@/components/forms/ApiAutocomplete.vue';
import DialogForm from '@/components/forms/DialogForm.vue';
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';

const emit = defineEmits(['create:obj']);

const { t } = useI18n();
const store = useStore();
const { education, project, projectPlaces, disciplineMap } = storeToRefs(store);

const step = ref(1);
const found = ref(null);
const disciplines = ref<number[]>([]);
const obj = ref({
  name: '',
  code: '',
});

function placeMapper(data: ApiObject[]) {
  return data.map((obj) => ({
    id: obj.id,
    name: (obj as Place).name,
    caption: `${(obj as Place).Type?.name}`,
    disable: placeIdsUsed.value.has(obj.id),
  }));
}

function addProjectPlace() {
  if (!project.value || !found.value || !disciplines.value.length) {
    return;
  }

  const data = {
    place_id: (found.value as Place).id,
    disciplines: disciplines.value,
  };

  api.post(project.value.rel_places, data).then((res) => {
    res.data.Disciplines = disciplines.value.map((id: number) => disciplineMap.value.get(id));
    store.createObj('projectPlace', res.data);
    notify.success(t('form.place.create.success'));
    emit('create:obj');
  });
}

function createPlace() {
  api.post((education.value as Education).rel_places, obj.value).then((res) => {
    api
      .post((project.value as Project).rel_places, {
        place_id: res.data.id,
        disciplines: disciplines.value,
      })
      .then((res) => {
        res.data.Disciplines = disciplines.value.map((id: number) => disciplineMap.value.get(id));
        store.createObj('projectPlace', res.data);
        notify.success(t('form.place.create.success'));
        emit('create:obj');
      });
  });
}

/**
 * Returns a set of place IDs used by the current project.
 * @returns {Set<number>}
 */
const placeIdsUsed = computed<Set<number>>(() => {
  return projectPlaces.value.reduce((set, obj) => {
    set.add(obj.place.id);
    return set;
  }, new Set<number>());
});
</script>
