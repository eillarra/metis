<template>
  <dialog-form :icon="iconAdd" :title="$t('contact')">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" :title="$t('form.contact.create.add_existing')" :icon="iconSearch" :active-icon="iconSearch">
          {{ $t('form.contact.create.search') }}
          <div class="q-gutter-sm q-mt-sm">
            <div class="row q-col-gutter-lg q-pt-sm">
              <q-checkbox v-model="formData.is_mentor" :label="t('mentor')" class="col-6 col-md-3" />
              <q-checkbox
                v-if="education?.configuration?.place_contact_is_staff"
                v-model="formData.is_staff"
                :label="t('staff')"
                class="col-6 col-md-3"
              />
              <q-checkbox v-model="formData.is_admin" :label="t('admin')" class="col-6 col-md-3" />
            </div>
            <readonly-field v-if="parent" :label="$t('place')" :value="parent.name" />
            <api-autocomplete
              v-else
              v-model="formData.place"
              clearable
              :data-source="projectPlaces"
              :mapper="placeMapper"
              :label="$t('place')"
            />
            <api-autocomplete
              v-model="formData.user"
              clearable
              data-source="/users/"
              :mapper="userMapper"
              :label="$t('contact')"
            />
          </div>
          <q-stepper-navigation class="flex">
            <q-btn
              unelevated
              @click="step = 2"
              color="blue-1"
              text-color="ugent"
              :label="$t('form.skip')"
              :disable="!!formData.user"
            />
            <q-space />
            <q-btn
              unelevated
              @click="addContact"
              color="ugent"
              :label="$t('form.add_to_place')"
              :disable="!selectedPlace || !formData.user"
            />
          </q-stepper-navigation>
        </q-step>
        <q-step :name="2" :title="$t('form.contact.create.new')" :icon="iconEmail" :active-icon="iconEmail">
          <div v-if="education?.configuration?.place_contact_welcome_email">
            {{ $t('form.contact.create.create_and_welcome') }}
          </div>
          <div v-else>{{ $t('form.contact.create.create_no_welcome') }}</div>
          <div class="q-gutter-sm q-mt-sm">
            <div class="row q-col-gutter-lg q-pt-sm">
              <q-checkbox v-model="formData.is_mentor" :label="t('mentor')" class="col-6 col-md-3" />
              <q-checkbox
                v-if="education?.configuration?.place_contact_is_staff"
                v-model="formData.is_staff"
                :label="t('staff')"
                class="col-6 col-md-3"
              />
              <q-checkbox v-model="formData.is_admin" :label="t('admin')" class="col-6 col-md-3" />
            </div>
            <readonly-field v-if="parent" :label="$t('place')" :value="parent.name" />
            <api-autocomplete
              v-else
              v-model="formData.place"
              clearable
              :data-source="(project as Project).rel_places"
              :mapper="placeMapper"
              :label="$t('place')"
            />
            <q-input v-model="formData.name" dense :label="$t('field.name')" type="text" />
            <q-input v-model="formData.email" dense :label="$t('field.email')" type="email" />
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
          @click="createContact"
          color="ugent"
          :label="$t('form.create')"
          :disable="!selectedPlace || !formData.name || !formData.email"
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
import ReadonlyField from '@/components/forms/ReadonlyField.vue';

import { iconAdd, iconEmail, iconSearch } from '@/icons';

const emit = defineEmits(['create:obj']);

const props = defineProps<{
  parent?: Place;
}>();

const { t } = useI18n();
const store = useStore();
const { education, project, places, projectPlaces } = storeToRefs(store);

const step = ref(1);
const formData = ref({
  user: null as QuasarAutocompleteOption | null,
  place: null as QuasarAutocompleteOption | null,
  name: null as string | null,
  email: null as string | null,
  is_mentor: false,
  is_staff: false,
  is_admin: false,
});

const selectedPlace = computed<Place | null>(() => {
  if (props.parent) return props.parent;
  if (!formData.value.place) return null;
  return places.value.find((obj) => obj.id === formData.value.place?.id) as Place;
});

function placeMapper(data: ApiObject[]) {
  return data.map((obj) => {
    const place: Place = (obj as ProjectPlace).place;
    return {
      id: place.id,
      name: place.name,
      caption: `${place.Type?.name}`,
    };
  });
}

function userMapper(data: ApiObject[]) {
  return data.map((obj) => ({
    id: obj.id,
    name: (obj as UserTiny).name,
    caption: (obj as UserTiny).email,
    disable: userIdsUsedByPlaceContacts.value.get(selectedPlace.value?.id as number)?.has(obj.id),
  }));
}

function addContact() {
  if (!selectedPlace.value || !formData.value.user) return;

  const data = {
    place_id: selectedPlace.value.id,
    user_id: formData.value.user.id,
    is_mentor: formData.value.is_mentor,
    is_staff: formData.value.is_staff,
    is_admin: formData.value.is_admin,
  };

  api.post(selectedPlace.value.rel_contacts, data).then((res) => {
    store.createObj('contact', res.data);
    notify.success(t('form.contact.create.success'));
    emit('create:obj');
  });
}

function createContact() {
  if (!selectedPlace.value) return;

  api
    .get('/users/', {
      params: {
        search: formData.value.email,
      },
    })
    .then((res) => {
      if (res.data.results.length > 0) {
        formData.value.user = res.data.results[0];
        step.value = 1;
        notify.warning(t('form.contact.create.exists_warning'));
        return;
      }

      const data = {
        name: formData.value.name,
        emails: [formData.value.email],
        project_id: project.value?.id || null,
        data: {
          is_mentor: formData.value.is_mentor,
          is_staff: formData.value.is_staff,
          is_admin: formData.value.is_admin,
        },
      };

      api.post(`${selectedPlace.value?.self}invite/`, data).then((res) => {
        store.createObj('contact', res.data);
        notify.success(t('form.contact.create.success'));
        emit('create:obj');
      });
    });
}

/**
 * Returns a map of place IDs to a set of user IDs used by the contacts of each place.
 * @returns {Map<number, Set<number>>}
 */
const userIdsUsedByPlaceContacts = computed<Map<number, Set<number>>>(() => {
  return places.value.reduce((map, obj) => {
    if (!obj.contacts || !obj.contacts.length) {
      return map;
    }
    map.set(
      obj.id,
      obj.contacts.reduce((set, contact) => {
        set.add(contact.user.id);
        return set;
      }, new Set<number>()),
    );
    return map;
  }, new Map());
});
</script>
