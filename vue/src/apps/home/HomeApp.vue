<template>
  <ugent-banner title="Metis" :subtitle="$t('home.presentation')">
    <template #default>
      <ugent-btn v-if="user" :label="$t('user_menu.dashboard')" color="yellow" :href="`/${$i18n.locale}/dashboard/`" />
      <div v-else class="fit column justify-between">
        <form method="post" action="/u/ugent/login/" class="q-mb-xl">
          <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken">
          <ugent-btn :label="$t('home.oauth_login')" color="yellow" type="submit" />
        </form>
        <ugent-link-list title="Help" :items="links" />
      </div>
    </template>
    <template #image>
      <img src="@/assets/uzgent.jpg" />
    </template>
  </ugent-banner>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { usePage } from '@inertiajs/vue3';

import UgentBanner from '@/components/UgentBanner.vue';
import UgentBtn from '@/components/UgentBtn.vue';
import UgentLinkList from '@/components/UgentLinkList.vue';

const { t } = useI18n();
const page = usePage();

const user = computed<DjangoAuthenticatedUser>(() => page.props.django_user as DjangoAuthenticatedUser);
const csrfToken = computed<string>(() => page.props.django_csrf_token as string);

const links = [
  {
    label: t('home.help.dict_login'),
    href: `https://helpdesk.ugent.be/account/${page.props.django_locale == 'en' ? 'en/' : ''}login.php`,
    target: '_blank',
  },
  {
    label: t('home.help.dict_externe'),
    href: `https://helpdesk.ugent.be/account/${page.props.django_locale == 'en' ? 'en/' : ''}externe.php`,
    target: '_blank',
  }
];
</script>
