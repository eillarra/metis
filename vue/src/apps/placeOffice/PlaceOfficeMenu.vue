<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'dashboard' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="business" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('place') }}</q-item-section>
        </q-item>
      </q-list>
      <q-list v-if="userIsAdmin" :dense="$q.screen.gt.sm">
        <q-item-label header>{{ $t('settings') }}</q-item-label>
        <!--<q-item clickable :to="{ name: 'address' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="place" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>information</q-item-section>
        </q-item>-->
        <q-item clickable :to="{ name: 'contacts' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="portrait" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('contact', 9) }}</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from './store';

const { userIsAdmin } = storeToRefs(useStore());
</script>
