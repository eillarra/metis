<template>
  <h6 class="q-mt-none q-mb-md">
    Status: <strong>{{ obj.status }}</strong>
  </h6>
  <q-list bordered separator class="q-mt-md">
    <q-item v-if="['preplanning', 'concept'].includes(obj.status)">
      <q-item-section class="q-py-sm">
        <q-item-label
          >Deze stage is <strong class="text-red">nog niet definitief</strong>. Enkel definitieve en 'goedgekeurde'
          stages zullen zichtbaar zijn voor studenten. Het wijzigen van de status naar definitief zal een
          aanvaardingsmail sturen naar de stageplaats beheerder(s).</q-item-label
        >
      </q-item-section>
      <q-item-section side center class="q-py-sm">
        <q-btn
          :disable="!obj.project_place"
          @click="updateStatus('definitive')"
          outline
          color="ugent"
          label="Zet stage als 'definitief'"
        />
      </q-item-section>
    </q-item>
    <q-item v-if="obj.status == 'definitive'">
      <q-item-section class="q-py-sm">
        <q-item-label
          >Deze stage is <strong class="text-ugent">definitief</strong>
          <strong v-if="obj.is_approved" class="text-ugent"> en goedgekeurd.</strong
          ><span v-else
            ><strong class="text-red"> maar nog niet goedgekeurd</strong>. Je kan een herinnering sturen naar de
            stageplaats beheerders om de stage goed te keuren.</span
          ></q-item-label
        >
        <q-item-label caption v-if="!obj.is_approved"
          >Let op: in elk geval worden er op maandagochtend herinneringen gestuurd naar alle stages die nog niet
          goedgekeurd zijn.</q-item-label
        >
      </q-item-section>
      <q-item-section side center class="q-py-sm">
        <q-btn
          v-if="!obj.is_approved"
          @click="sendEmail('internship.approve')"
          outline
          color="ugent"
          label="Herinnering sturen"
        />
      </q-item-section>
    </q-item>
    <q-item v-if="obj.status == 'definitive'">
      <q-item-section class="q-py-sm">
        <q-item-label
          >Als de stage geannuleerd wordt maar je wil deze toch in de lijst van stages houden voor historische redenen,
          kan je de status gewoon op 'geannuleerd' zetten.</q-item-label
        >
      </q-item-section>
      <q-item-section side center class="q-py-sm">
        <q-btn
          @click="updateStatus('cancelled', t('form.internship.confirm_cancel'))"
          outline
          color="ugent"
          label="Zet stage als 'geannuleerd'"
        />
      </q-item-section>
    </q-item>
    <q-item v-if="obj.status == 'cancelled'">
      <q-item-section class="q-py-sm">
        <q-item-label>Je kan altijd de stage terug activeren door de status op 'definitief' te zetten.</q-item-label>
      </q-item-section>
      <q-item-section side center class="q-py-sm">
        <q-btn @click="updateStatus('definitive')" outline color="ugent" label="Zet stage als 'definitief'" />
      </q-item-section>
    </q-item>
    <q-item v-if="obj.status == 'unsuccessful'">
      <q-item-section class="q-py-sm text-grey">
        <q-item-label>Geen acties om te ondernemen.</q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
  <h6 class="q-mt-lg q-mb-md">Danger zone</h6>
  <q-list bordered separator>
    <q-item v-if="obj.student">
      <q-item-section class="q-py-sm">
        <q-item-label
          >Je kan {{ obj.Student?.User?.name }} verwijderen van deze stage. Dit zal de stage zelf niet
          verwijderen.</q-item-label
        >
      </q-item-section>
      <q-item-section side center class="q-py-sm">
        <q-btn @click="deleteStudent" outline color="red" :label="$t('form.student.delete')" />
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section class="q-py-sm">
        <q-item-label>Stage verwijderen en uit de lijst halen. </q-item-label>
      </q-item-section>
      <q-item-section side center class="q-py-sm">
        <q-btn @click="deleteInternship" outline color="red" :label="$t('form.internship.delete')" />
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';

import { useStore } from '../../store.js';

const emit = defineEmits(['delete:obj']);

const props = defineProps<{
  internship: Internship;
}>();

const { t } = useI18n();
const store = useStore();

const { education } = storeToRefs(store);

const obj = ref<Internship>(props.internship);

function setStatus(status: string) {
  obj.value.status = status;

  if (
    status == 'definitive' &&
    education.value?.configuration?.automatic_internship_approval &&
    !obj.value.is_approved
  ) {
    obj.value.is_approved = true;
  }

  save().then(() => {
    if (status == 'definitive') {
      if (education.value?.configuration?.automatic_internship_approval && obj.value.is_approved) {
        sendEmail('internship.definitive');
        sendEmail('internship.approved');
      } else if (!education.value?.configuration?.automatic_internship_approval && !obj.value.is_approved) {
        sendEmail('internship.approve');
      }
    }
  });
}

function updateStatus(status: string, confirmMessage?: string) {
  if (confirmMessage) {
    confirm(confirmMessage, () => {
      setStatus(status);
    });
  } else {
    setStatus(status);
  }
}

function save() {
  return api.put(obj.value.self, obj.value).then((res) => {
    obj.value.updated_at = res.data.updated_at;
    obj.value.updated_by = res.data.updated_by;
    store.updateObj('projectInternship', obj.value);
    notify.success(t('form.internship.saved'));
  });
}

function sendEmail(code: string) {
  return api.post(`${obj.value.self}send_email/`, { code: code }).then(() => {
    notify.success(t('form.email_sent'));
  });
}

function deleteInternship() {
  confirm(t('form.internship.confirm_delete'), () => {
    api.delete(obj.value.self).then(() => {
      store.deleteObj('projectInternship', obj.value);
      notify.success(t('form.internship.deleted'));
      emit('delete:obj');
    });
  });
}

function deleteStudent() {
  confirm(t('form.internship.confirm_delete_student'), () => {
    api.patch(obj.value.self, { student: null }).then(() => {
      obj.value.student = null;
      obj.value.Student = undefined;
      store.updateObj('projectInternship', obj.value);
      notify.success(t('form.internship.deleted_student'));
    });
  });
}
</script>
