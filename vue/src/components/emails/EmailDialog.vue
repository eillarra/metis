<template>
  <full-dialog icon="mail_outline" :title="$t('field.email')" class="small" hide-drawer>
    <template #tabs>
      <table class="q-px-md q-py-sm q-mt-md q-mb-lg bg-grey-2 full-width">
        <tr>
          <td><strong>{{ $t('field.sent_at') }}:</strong></td>
          <td>{{ formatDate(email.sent_at) }}</td>
        </tr>
        <tr>
          <td><strong>{{ $t('field.sent_to') }}:</strong></td>
          <td>
            <span>{{ toNameEmails }}</span>
            <i
              @click="copyText(toNameEmails)"
              class="q-icon notranslate material-icons cursor-pointer q-ml-xs"
              :style="{ 'font-size': '14px' }"
              aria-hidden="true"
              role="presentation"
            >content_copy</i>
          </td>
        </tr>
        <tr>
          <td><strong>{{ $t('field.subject') }}:</strong></td>
          <td>{{ email.subject }}</td>
        </tr>
      </table>
    </template>
    <template #page>
      <div class="q-mx-lg">
        <markdown-toast-viewer v-model="dummyBody" :source-text="email.body" class="q-px-md" />
      </div>
    </template>
    <template #footer> </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { copyToClipboard } from 'quasar';

import { api } from '@/axios.ts';
import { notify } from '@/notify';
import { formatDate } from '@/utils/dates';

import FullDialog from '@/components/FullDialog.vue';
import MarkdownToastViewer from '@/components/forms/MarkdownToastViewer.vue';

const { t } = useI18n();

const props = defineProps<{
  obj: Email;
  internships?: Internship[];
}>();

const dummyBody = ref<string>('');
const extraData = ref();
const email = computed<FullEmail>(() => ({
  ...props.obj,
  ...extraData.value,
}));

const toNameEmails = computed<string>(() => {
  // if extraData.value is not yet set, return the original value
  if (!extraData.value) {
    return props.obj.to.join(', ');
  }
  // else look the extraData.internship.mentors data and return matching names and emails, or just original email
  return props.obj.to
    .map((to: string) => {
      const mentor: Mentor | undefined = extraData.value.internship?.mentors.find(
        (mentor: Mentor) => mentor.user.email === to
      );
      return mentor ? `${mentor.user.name} <${mentor.user.email}>` : to;
    })
    .join(', ');
});

function copyText(text: string) {
  copyToClipboard(text).then(() => {
    notify.info(t('copied_to_clipboard'));
  });
}

function fetchEmail() {
  api.get(props.obj.self).then((response) => {
    extraData.value = response.data;
  });
}


onMounted(() => {
  fetchEmail();
});
</script>
