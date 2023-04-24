<template>
  <ugent-banner
    title="Metis"
    subtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
  >
    <template #default>
      <ugent-btn v-if="user" :label="$t('menu.dashboard')" color="yellow" :href="`/${$i18n.locale}/dashboard/`" />
      <div v-else class="fit column justify-between">
        <div class="q-mb-xl">
          <ugent-btn :label="$t('home.oauth_login')" color="yellow" href="/u/ugent/login/?process=login" />
        </div>
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

const user = computed(() => page.props.django_user);

const links = [
  {
    label: t('home.help.no_account'),
    href: '/u/login/',
  },
];
</script>
