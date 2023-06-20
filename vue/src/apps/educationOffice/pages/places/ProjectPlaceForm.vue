<template>
  <dialog-form icon="business" :title="obj.place.name">
    <template #tabs>
      <q-tabs v-model="tab" dense shrink inline-label no-caps>
        <q-tab name="info" label="Info" icon="info_outline" />
        <q-tab name="availability" :label="$t('availability')" icon="tag" />
        <q-tab name="contacts" :label="$t('contact', 9)" icon="portrait" />
        <q-tab
          v-if="education?.configuration?.place_text_types.length"
          name="texts"
          :label="$t('text', 9)"
          icon="notes"
        />
        <q-tab name="remarks" :label="`${$t('remark', 9)} (${remarkCount})`" icon="chat_bubble_outline" />
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
            <place-type-select
              v-if="education"
              v-model="obj.place.type"
              :place-types="education.place_types"
              :label="$t('place_type')"
            />
          </div>
        </q-tab-panel>
        <q-tab-panel name="availability">
          <div v-for="period in project?.periods" :key="period.id" class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              {{ period.ProgramInternship?.Block?.name }} / {{ period.ProgramInternship?.name }}<br />
              {{ period.start_date }} - {{ period.end_date }}
            </div>
            <q-input
              v-model="availability[String(period.id)].min"
              dense
              label="min"
              type="number"
              class="col-6 col-md-3"
            />
            <q-input
              v-model="availability[String(period.id)].max"
              dense
              label="max"
              type="number"
              class="col-6 col-md-3"
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
        <q-tab-panel name="texts">
          <texts-view
            v-if="textsEndpoint"
            container
            :api-endpoint="textsEndpoint"
            :text-types="education?.configuration?.place_text_types as TextEntryType[]"
          />
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
        <q-btn
          @click="deletePlace"
          outline
          color="red"
          :label="$t('form.place.delete')"
          :disable="projectPlacesWithInternships.has(obj.id)"
        />
        <q-space />
        <q-btn
          @click="save"
          unelevated
          color="ugent"
          :label="$t('form.place.save')"
          :disable="!obj.place.name || !obj.place.code || !obj.disciplines.length"
        />
      </div>
      <div v-else-if="tab == 'availability'" class="flex q-gutter-sm q-pa-lg">
        <q-space />
        <q-btn @click="updateAvailability" unelevated color="ugent" :label="$t('form.update')" />
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
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';
import UpdatedByView from '@/components/forms/UpdatedByView.vue';
import RemarksView from '@/components/rel/RemarksView.vue';
import TextsView from '@/components/rel/TextsView.vue';
import PlaceTypeSelect from '../../components/PlaceTypeSelect.vue';

const { t } = useI18n();
const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: ProjectPlace;
}>();

const store = useStore();
const { education, project, projectPlacesWithInternships, disciplineMap } = storeToRefs(store);

const obj = ref<ProjectPlace>(props.obj);
const tab = ref<string>('info');
const projectName = computed<string>(() => (project.value ? project.value.name : ''));
const availability = ref<Record<string, { min: number; max: number }>>(
  reformatAvailability(obj.value.availability_set, project.value)
);

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

const textsEndpoint = computed<null | ApiEndpoint>(() => {
  if (!props.obj) return null;
  return props.obj.place.rel_texts;
});

function syncProjectPlaceInfo(data: ProjectPlace) {
  data.Disciplines = data.disciplines.map((id: number) => disciplineMap.value.get(id)) as Discipline[];
  data.place.Type = education.value?.place_types.find((type) => type.id === data.place.type) as PlaceType;
  obj.value = data;
  store.updateObj('projectPlace', obj.value);
}

function save() {
  api
    .put(obj.value.place.self, {
      ...obj.value.place,
    })
    .then(() => {
      api
        .put(obj.value.self, {
          ...obj.value,
          place_id: obj.value.place.id,
        })
        .then((res) => {
          syncProjectPlaceInfo(res.data);
          notify.success(t('form.place.saved'));
        });
    });
}

function updateAvailability() {
  const data = Object.keys(availability.value).map((key) => ({
    period: +key,
    min: availability.value[key].min,
    max: availability.value[key].max,
  }));

  api.put(`${obj.value.self}availability/`, data).then((res) => {
    syncProjectPlaceInfo(res.data);
    notify.success(t('form.place.saved'));
  });
}

function deletePlace() {
  confirm(t('form.place.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      store.deleteObj('projectPlace', obj.value);
      notify.success(t('form.place.deleted'));
      emit('delete:obj');
    });
  });
}

function deleteContact(contact: Contact) {
  confirm(t('form.contact.confirm_delete'), () => {
    api.delete(contact.self).then(() => {
      obj.value.place.contacts = obj.value.place.contacts.filter((c) => c.id !== contact.id);
      store.updateObj('projectPlace', obj.value);
      notify.success(t('form.contact.deleted'));
    });
  });
}

function reformatAvailability(
  availabilitySet: ProjectPlaceAvailability[],
  project?: Project
): Record<string, { min: number; max: number }> {
  const availability = availabilitySet.reduce((acc, cur) => {
    acc[cur.period] = { min: cur.min, max: cur.max };
    return acc;
  }, {} as Record<string, { min: number; max: number }>);

  project?.periods.forEach((period) => {
    if (!availability[period.id]) {
      availability[period.id] = { min: 0, max: 0 };
    }
  });

  return availability;
}
</script>
