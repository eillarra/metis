<template>
  <dialog-form icon="calendar_month" :title="internshipName">
    <template #page>
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" title="Plaats toevoegen" icon="business" active-icon="edit">
          <div v-if="obj.Place">
            <div class="text-h text-weight-bold q-my-sm">{{ obj.Place?.name }}</div>
            Stageplaats is toegekend.
          </div>
          <div v-else>
            <p>
              Voeg de contactgegevens toe van de huisarts die je mentor zal zijn. Deze gegevens zullen gebruikt worden
              om een account aan te maken, dus zorg ervoor dat het emailadres correct is.
            </p>
            <form @submit.prevent.stop="proposePlace" class="q-gutter-sm q-mt-sm">
              <q-input v-model="formData.place_contact_name" dense :label="$t('contact')" />
              <q-input v-model.trim="formData.place_contact_email" dense :label="$t('field.email')" type="email" />
              <q-input
                v-model="formData.place_contact_phone_number"
                dense
                :label="$t('field.phone_number')"
                type="tel"
              />
              <p class="q-mt-xl">
                Indien de arts een andere naam heeft voor zijn/haar praktijk, gelieve deze hier aan te geven:
              </p>
              <q-input v-model="formData.place_name" dense :label="$t('place')" />
              <q-input v-model="formData.place_address" dense :label="$t('address')" />
              <q-btn
                type="submit"
                unelevated
                color="ugent"
                :label="$t('form.internship.propose_place')"
                :disable="!formData.place_contact_name || !formData.place_contact_email"
              />
            </form>
          </div>
        </q-step>
      </q-stepper>
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
      notify.success(t('form.internship.saved'));
      obj.value = res.data;
    })
    .finally(() => {
      sending.value = false;
    });
}
</script>
