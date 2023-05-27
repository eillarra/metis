<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'tasks' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="checklist" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('task', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('user_menu.history') }}</q-item-label>
        <!--<q-item clickable :to="{ name: 'internships' }" active-class="bg-ugent text-white">-->
        <q-item disabled>
          <q-item-section avatar>
            <q-icon name="calendar_month" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('internship', 9) }}</q-item-section>
        </q-item>
        <q-item
          clickable
          :to="{ name: 'signatures' }"
          active-class="bg-ugent text-white"
          :disable="!signatures || !signatures.length"
        >
          <q-item-section avatar>
            <q-icon name="draw" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('signature', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('user_menu.account') }}</q-item-label>
        <!--<q-item clickable :to="{ name: 'contact_details' }" active-class="bg-ugent text-white">-->
        <q-item disabled>
          <q-item-section avatar>
            <q-icon name="import_contacts" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('user_menu.contact_details') }}</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from './store';

const { signatures } = storeToRefs(useStore());
</script>
