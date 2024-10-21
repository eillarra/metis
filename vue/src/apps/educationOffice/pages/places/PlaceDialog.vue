<template>
  <full-dialog icon="task_alt" :title="obj.place.name">
    <template #menu>
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('place') }}</q-item-label>
        <q-item clickable @click="tab = 'info'" :active="tab == 'info'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="info_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Info</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'contacts'" :active="tab == 'contacts'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="portrait" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('contact', 9) }}</q-item-section>
        </q-item>
        <q-item
          clickable
          @click="tab = 'availability'"
          :active="tab == 'availability'"
          active-class="bg-ugent text-white"
        >
          <q-item-section avatar>
            <q-icon name="tag" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('availability') }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'addresses'" :active="tab == 'addresses'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="map" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('address', 9) }}</q-item-section>
        </q-item>
        <q-item clickable @click="tab = 'documents'" :active="tab == 'documents'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="drive_file_move_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('other') }}</q-item-label>
        <q-item clickable @click="tab = 'remarks'" :active="tab == 'remarks'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="hasRemarks ? iconChatBadge : iconChat" size="xs" />
          </q-item-section>
          <q-item-section>{{ $t('remark', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>Logs</q-item-label>
        <q-item clickable @click="tab = 'emails'" :active="tab == 'emails'" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="mail_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('field.email', 9) }}</q-item-section>
        </q-item>
      </q-list>
    </template>
    <template #page>
      <q-tab-panels v-model="tab" class="q-pb-lg">
        <q-tab-panel name="info">
          <div class="q-gutter-sm">
            <readonly-field :value="project?.name || ''" :label="$t('project')" />
            <q-input v-model="obj.place.name" dense :label="$t('field.name')" />
            <q-input v-model="obj.place.code" dense :label="$t('field.code')" />
            <discipline-select
              v-if="education"
              v-model="obj.disciplines"
              multiple
              :disciplines="education.disciplines"
              :label="$t('discipline', 9)"
            />
            <place-option-select
              v-if="education && education.place_locations.length"
              v-model="obj.place.location"
              :place-types="education.place_locations"
              :label="$t('place_location')"
            />
            <place-option-select
              v-if="education && education.place_types.length"
              v-model="obj.place.type"
              :place-types="education.place_types"
              :label="$t('place_type')"
            />
            <q-select
              v-model="obj.place.default_language"
              dense
              :label="$t('language')"
              :options="languageOptions"
              options-dense
              emit-value
              map-options
            />
            <q-toggle
              v-model="obj.place.is_flagged"
              :label="$t('form.place.add_flag')"
              left-label
              color="orange"
              class="q-mt-lg"
              checked-icon="flag"
            />
            <div v-if="obj.place.is_flagged" class="text-caption">{{ $t('check_remarks') }}</div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="availability">
          <div v-for="period in project?.periods" :key="period.id" class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              {{ period.ProgramInternship?.Block?.name }} / {{ period.ProgramInternship?.name }}<br />
              {{ period.start_date }} - {{ period.end_date }}
            </div>
            <q-input
              v-model.number="availability[String(period.id)].min"
              dense
              label="min"
              type="number"
              class="col-6 col-md-3"
            />
            <q-input
              v-model.number="availability[String(period.id)].max"
              dense
              label="max"
              type="number"
              class="col-6 col-md-3"
            />
          </div>
        </q-tab-panel>
        <q-tab-panel name="contacts">
          <place-contacts :obj="obj" />
        </q-tab-panel>
        <q-tab-panel name="addresses">
          <address-cards :api-endpoint="obj.place.rel_addresses" in-dialog />
        </q-tab-panel>
        <q-tab-panel name="remarks">
          <remarks-view :api-endpoints="remarkEndpoints" :visibility-options="['student']"/>
        </q-tab-panel>
        <q-tab-panel name="documents">
          <files-view :api-endpoint="obj.place.rel_files">
            <template #custom-fields="scope">
              {{ scope.formData }}
            </template>
          </files-view>
        </q-tab-panel>
        <q-tab-panel name="emails">
          <div class="row q-col-gutter-lg q-mb-none">
            <h4 class="col-12 col-md-6 q-mt-none q-mb-lg">
              {{ $t('field.email', 9) }}
            </h4>
          </div>
          <emails-view :emails="emails" :tags="[`place.id:${obj.place.id}`]" in-dialog />
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
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { confirm } from '@/dialog';
import { notify } from '@/notify';
import { useStore } from '../../store.js';

import FullDialog from '@/components/FullDialog.vue';
import EmailsView from '@/components/emails/EmailsView.vue';
import DisciplineSelect from '@/components/forms/DisciplineSelect.vue';
import ReadonlyField from '@/components/forms/ReadonlyField.vue';
import AddressCards from '@/components/rel/AddressCards.vue';
import FilesView from '@/components/rel/FilesView.vue';
import RemarksView from '@/components/rel/RemarksView.vue';
import PlaceContacts from './PlaceContacts.vue';
import PlaceOptionSelect from '../../components/PlaceOptionSelect.vue';

import { iconChat, iconChatBadge } from '@/icons';

const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  obj: ProjectPlace;
}>();

const { t } = useI18n();
const store = useStore();
const { education, emails, project, projectPlacesWithInternships, disciplineMap } = storeToRefs(store);

const tab = ref('info');
const obj = ref<ProjectPlace>(props.obj);

const hasRemarks = computed<boolean>(() => (Number(obj.value.place._tags_dict?.['remarks.count']) || 0) > 0);
const remarkEndpoints = computed<null | Record<string, ApiEndpoint>>(() => {
  if (!props.obj) return null;
  return {
    default: props.obj.place.rel_remarks,
  };
});

// ----- CHECK BELOW HERE -----

const availability = ref<Record<string, { min: number; max: number }>>(
  reformatAvailability(obj.value.availability_set, project.value),
);

const languageOptions = computed<QuasarSelectOption[]>(() => {
  return [
    { value: 'nl', label: 'Nederlands' },
    { value: 'en', label: 'English' },
  ];
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

function reformatAvailability(
  availabilitySet: ProjectPlaceAvailability[],
  project?: Project,
): Record<string, { min: number; max: number }> {
  const availability = availabilitySet.reduce(
    (acc, cur) => {
      acc[cur.period] = { min: cur.min, max: cur.max };
      return acc;
    },
    {} as Record<string, { min: number; max: number }>,
  );

  project?.periods.forEach((period) => {
    if (!availability[period.id]) {
      availability[period.id] = { min: 0, max: 0 };
    }
  });

  return availability;
}
</script>
