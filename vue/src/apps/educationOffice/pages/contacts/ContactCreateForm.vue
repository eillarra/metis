<template>
  <dialog-form icon="add" :title="$t('contact')">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive>
        <q-step :name="1" :title="$t('form.contact.create.add_existing')" icon="search" active-icon="search">
          {{ $t('form.contact.create.search') }}
          <div class="q-gutter-sm q-mt-sm">
            <div class="row q-col-gutter-lg q-pt-sm">
              <q-checkbox v-model="formData.is_mentor" :label="t('mentor')" class="col-6 col-md-3" />
              <q-checkbox v-model="formData.is_staff" :label="t('staff')" class="col-6 col-md-3" />
            </div>
            <api-autocomplete
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
              :disable="!formData.user || !formData.place"
            />
          </q-stepper-navigation>
        </q-step>
        <q-step :name="2" :title="$t('form.contact.create.new')" icon="mail_outline" active-icon="mail_outline">
          {{ $t('form.contact.create.invite') }}
          <div class="q-gutter-sm q-mt-sm">
            <div class="row q-col-gutter-lg q-pt-sm">
              <q-checkbox v-model="formData.is_mentor" :label="t('mentor')" class="col-6 col-md-3" />
              <q-checkbox v-model="formData.is_staff" :label="t('staff')" class="col-6 col-md-3" />
            </div>
            <api-autocomplete
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
          @click="inviteContact"
          color="ugent"
          :label="$t('form.invite')"
          :disable="!formData.place || !formData.name || !formData.email"
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

const emit = defineEmits(['create:obj']);

const { t } = useI18n();
const store = useStore();
const { project, places, projectPlaces } = storeToRefs(store);

const step = ref(1);
const formData = ref({
  user: null as QuasarAutocompleteOption | null,
  place: null as QuasarAutocompleteOption | null,
  name: null as string | null,
  email: null as string | null,
  is_mentor: false,
  is_staff: false,
});

const selectedPlace = computed<Place | null>(() => {
  if (!formData.value.place) return null;
  return places.value.find((obj) => obj.id === formData.value.place?.id) as Place;
});

function placeMapper(data: ApiObject[]) {
  return data.map((obj) => {
    const place: Place = (obj as ProjectPlace).place;
    return {
      id: place.id,
      name: place.name,
      caption: `${place.type} / ${place.region?.name}`,
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
  };

  api.post(selectedPlace.value.rel_contacts, data).then((res) => {
    store.createObj('contact', res.data);
    notify.success(t('form.contact.create.saved'));
    emit('create:obj');
  });
}

function inviteContact() {
  if (!selectedPlace.value) return;

  const data = {
    type: 'contact',
    name: formData.value.name,
    email: formData.value.email,
    data: {
      is_mentor: formData.value.is_mentor,
      is_staff: formData.value.is_staff,
    },
  };

  api.post(`${selectedPlace.value.self}invite/`, data).then(() => {
    notify.success(t('form.contact.create.invited'));
    emit('create:obj');
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
      }, new Set<number>())
    );
    return map;
  }, new Map());
});
</script>
