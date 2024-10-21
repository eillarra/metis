<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'tasks' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconTasks" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('my_tasks') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'planning' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconCalendar" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('planning') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'documents' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconFiles" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('place') }}</q-item-label>
        <q-item clickable :to="{ name: 'contacts' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconContacts" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('contact', 9) }}</q-item-section>
        </q-item>
        <q-item clickable v-if="userIsAdmin" :to="{ name: 'addresses' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconMap" size="xs"></q-icon>
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

import { iconCalendar, iconContacts, iconFiles, iconMap, iconTasks } from '@/icons';

const { userIsAdmin } = storeToRefs(useStore());
</script>
