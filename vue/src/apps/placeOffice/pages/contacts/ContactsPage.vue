<template>
  <div v-if="place">
    <h3 class="text-ugent col-12 col-md-3 q-mb-lg">{{ $t('contact', 9) }}</h3>
    <contacts-table :contacts="place.contacts" />
    <div class="row q-col-gutter-x-xl q-col-gutter-y-lg q-mb-xl">
      <div class="col-12 col-sm-6 col-md-4">
        <h5 class="q-mt-none q-mb-md">
          Wat is een <span class="text-lowercase">{{ $t('admin') }}</span
          >?
        </h5>
        <p>
          De <span class="text-lowercase">{{ $t('admin') }}</span> (één person) kan de informatie van de stageplaats
          (kledij, patiëntenpopulatie, bereikbaarheid, werkrooster, …) rechtstreeks in METIS aanpassen. Dus niet meer op
          papier en via e-mail zoals voorheen.
        </p>
      </div>
      <div v-if="userIsAdmin" class="col-12 col-sm-6 col-md-4">
        <h5 class="q-mt-none q-mb-md">Ontbrekende collega's?</h5>
        <p>
          Zijn er nog collega's die ontbreken in bovenstaande lijst. Gelieven hun naam en e-mailadres door te geven. We
          sturen hen dan ook een uitnodiging om een account aan te maken.
        </p>
      </div>
      <div v-if="userIsAdmin" class="col-12 col-md-4">
        <q-btn
          outline
          color="ugent"
          :label="$t('form.send_email_to', { email: education?.office_email })"
          :disable="emailSent"
          @click="dialogEmail = true"
        />
      </div>
    </div>
    <q-dialog v-if="userIsAdmin" v-model="dialogEmail">
      <dialog-form :icon="iconEmail" :title="$t('form.send_email_to', { email: education?.office_email })">
        <template #page>
          <div class="q-pa-lg">
            <q-input v-model="email" filled type="textarea" :disable="emailSent" />
          </div>
        </template>
        <template #footer>
          <q-btn
            unelevated
            @click="sendEmail"
            color="ugent"
            :label="$t('form.send_email')"
            :disable="!email"
            class="float-right q-ma-lg"
          />
        </template>
      </dialog-form>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { storeToRefs } from 'pinia';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

import ContactsTable from './ContactsTable.vue';
import DialogForm from '@/components/forms/DialogForm.vue';

import { iconEmail } from '@/icons';

const { education, place, admins, userIsAdmin } = storeToRefs(useStore());

const email = ref<string>('');
const emailSent = ref<boolean>(false);
const dialogEmail = ref<boolean>(false);

function sendEmail() {
  const url = '/user/contact/places/' + (place.value as Place).id + '/email/';
  const data = {
    text: email.value,
  };
  api.post(url, data).then(() => {
    notify.success('Hartelijke dank voor het doorsturen van de info.');
    emailSent.value = true;
    dialogEmail.value = false;
  });
}

watch(dialogEmail, (value) => {
  if (value) {
    let text = `De contactpersonen voor stageplaats ${(place.value as Place).name} zijn:\n\n`;
    for (const contact of (place.value as Place).contacts) {
      text += `- ${contact.user.name} <${contact.user.email}>\n`;
    }
    text += `\nDe admin-rol wordt opgenomen door: ${admins.value[0]?.user.name}`;
    email.value = text;
  }
});
</script>
