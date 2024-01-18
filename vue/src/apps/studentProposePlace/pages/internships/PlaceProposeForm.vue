<template>
  <dialog-form icon="calendar_month" :title="internshipName">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" title="Plaats toevoegen" icon="business" active-icon="edit">
          <div v-if="obj.Place">
            <div class="text-h text-weight-bold q-my-sm">{{ obj.Place?.name }}</div>
            Stageplaats is toegekend, gelieve het akkoord document te sturen naar
            <a mailto="metis.helpdesk@ugent.be">metis.helpdesk@ugent.be</a> (binnenkort kan dit online).
          </div>
          <div v-else>
            <p>
              Voeg de contactgegevens toe van de huisarts die je mentor zal zijn. Deze gegevens zullen gebruikt worden
              om een account aan te maken, dus zorg ervoor dat het emailadres correct is.
            </p>
            <p>
              Gelieve hierbij rekening te houden met de lijst van <strong>niet-te-contacteren praktijken</strong> (zie
              Infosite Master GK - Inhoudsopgave
              <a
                target="_blank"
                href="https://ufora.ugent.be/d2l/le/content/77826/Home?itemIdentifier=D2L.LE.Content.ContentObject.ModuleCO-56563"
                >2de Master GE</a
              >
              -
              <a
                target="_blank"
                href="https://ufora.ugent.be/d2l/le/content/77826/Home?itemIdentifier=D2L.LE.Content.ContentObject.ModuleCO-112404"
                >Seniorstages 2023 - 2024 - 2025</a
              >
              -
              <a
                target="_blank"
                href="https://ufora.ugent.be/d2l/le/content/77826/Home?itemIdentifier=D2L.LE.Content.ContentObject.ModuleCO-217751"
                >Seniorstage Huisartsgeneeskunde</a
              >).
            </p>
            <div class="q-gutter-sm q-mt-sm">
              <q-input v-model="formData.place_contact_name" dense :label="$t('contact')" />
              <q-input v-model.trim="formData.place_contact_email" dense :label="$t('field.email')" type="email" />
              <q-input v-model="formData.place_contact_phone_number" dense :label="$t('field.phone_number')" />
              <p class="q-mt-xl">
                Indien de arts een andere naam heeft voor zijn/haar praktijk, gelieve deze hier aan te geven:
              </p>
              <q-input v-model="formData.place_name" dense :label="$t('place')" />
              <q-input v-model="formData.place_address" dense :label="$t('address')" />
            </div>
          </div>
        </q-step>
      </q-stepper>
    </template>
    <template #footer>
      <div class="flex q-gutter-sm q-pa-lg">
        <q-space />
        <q-btn
          v-if="!obj.Place"
          unelevated
          @click="proposePlace"
          color="ugent"
          :label="$t('form.internship.propose_place')"
          :disable="!formData.place_contact_name || !formData.place_contact_email"
        />
      </div>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios.ts';
import { notify } from '@/notify';

import DialogForm from '@/components/forms/DialogForm.vue';

const { t } = useI18n();

const props = defineProps<{
  obj: Internship;
}>();

const obj = ref<Internship>(props.obj);
const internshipName = computed<string>(() => `${obj.value.Student?.User?.name} - (${obj.value.Discipline?.name})`);

const step = ref(1);
const formData = ref({
  internship_id: props.obj.id,
  place_name: '',
  place_contact_name: '',
  place_contact_email: '',
  place_contact_phone_number: '',
  place_address: '',
});

const sending = ref<boolean>(false);

function proposePlace() {
  sending.value = true;

  if (!formData.value.place_name) {
    formData.value.place_name = `Praktijk ${formData.value.place_contact_name}`;
  }

  api
    .post('/user/student/preplanned-internships/', formData.value)
    .then((res) => {
      notify.success(t('form.internship.approved'));
      obj.value = res.data;
    })
    .finally(() => {
      sending.value = false;
    });
}
</script>
