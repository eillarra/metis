<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'tasks' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="done_all" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('my_tasks') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'planning' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="calendar_month" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('planning') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'documents' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="drive_file_move_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('place') }}</q-item-label>
        <q-item clickable :to="{ name: 'contacts' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="portrait" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('contact', 9) }}</q-item-section>
        </q-item>
        <q-item clickable v-if="userIsAdmin" :to="{ name: 'addresses' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="map" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('address', 9) }}</q-item-section>
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
