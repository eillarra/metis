<template>
  <div v-if="place">
    <h3 class="text-ugent col-12 col-md-3 q-mb-xl">{{ $t('place') }}</h3>
    <p>
      U bent aangemeld als contactpersoon voor de stageplaats <strong>{{ place.name }}</strong
      >.
    </p>
    <p>In METIS zijn volgende personen gekend voor deze stageplaats:</p>
    <ul>
      <li v-for="contact in place.contacts" :key="contact.id">
        {{ contact.user.name }}, &lt;{{ contact.user.email }}&gt;
        <q-badge v-if="contact.is_mentor" outline color="ugent" class="q-ml-sm">Mentor</q-badge>
        <q-badge v-if="contact.is_admin" color="ugent" class="q-ml-sm">Admin</q-badge>
      </li>
    </ul>
    <p>Iedereen in deze lijst heeft een e-mail ontvangen met de vraag zich aan te melden.</p>
    <div v-if="!admins.length">
      <p class="bg-yellow-2">
        <strong>In een eerste stap</strong> wensen we de accounts voor METIS te actualiseren. Daarom vragen we u
        vriendelijk om onderstaande info aandachtig te lezen, het e-mailbericht aan te vullen en meteen te versturen.
      </p>
      <p>(U kan niets fout doen. De gegevens kunnen later gewijzigd en/of aangevuld worden indien nodig.)</p>
      <q-input filled dense type="textarea" v-model="email" autogrow :disable="emailSent" class="q-my-lg"></q-input>
      <q-btn
        unelevated
        @click="sendEmail"
        color="ugent"
        :label="$t('form.send_email')"
        :disable="!email || emailSent"
        class="q-mb-lg"
      />
      <div class="row q-col-gutter-xl q-mb-xl">
        <div class="col-12 col-md">
          <h5 class="q-mb-md">Wat is een admin?</h5>
          <p>
            De admin (één person) kan de informatie van de stageplaats (kledij, patiëntenpopulatie, bereikbaarheid,
            werkrooster, …) rechtstreeks in METIS aanpassen. Dus niet meer op papier en via e-mail zoals voorheen.
          </p>
        </div>
        <div class="col-12 col-md">
          <h5 class="q-mb-md">Ontbrekende collega's?</h5>
          <p>
            Zijn er nog collega's die ontbreken in bovenstaande lijst. Gelieven hun naam en e-mailadres door te geven.
            We sturen hen dan ook een uitnodiging om een account aan te maken.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { storeToRefs } from 'pinia';

import { api } from '@/axios';
import { notify } from '@/notify';

import { useStore } from '../store';

const { place, admins } = storeToRefs(useStore());

const emailSent = ref<boolean>(false);

function sendEmail() {
  const url = '/user/contact/places/' + (place.value as Place).id + '/email/';
  const data = {
    text: email.value,
  };
  api.post(url, data).then(() => {
    notify.success('Hartelijke dank voor het doorsturen van de info.');
    emailSent.value = true;
  });
}

// email

let text = `De contactpersonen voor stageplaats ${(place.value as Place).name} zijn:\n\n`;
for (const contact of (place.value as Place).contacts) {
  text += `- ${contact.user.name} <${contact.user.email}>\n`;
}
text += '\nDe admin-rol wordt opgenomen door: ';

const email = ref<string>(text);
</script>
