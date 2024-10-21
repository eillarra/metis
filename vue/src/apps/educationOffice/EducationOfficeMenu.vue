<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'planning' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconCalendar" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('allocation') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'students' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconStudent" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('student', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'places' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconPlace" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('place', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'placeContacts' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconContacts" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('contact', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'questionings' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconQuestioning" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('questioning', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'documents' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconFiles" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>Logs</q-item-label>
        <q-item clickable :to="{ name: 'emails' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconEmails" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('field.email', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('settings') }}</q-item-label>
        <q-item clickable :to="{ name: 'project' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconSettings" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('project') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'programs' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon :name="iconProgram" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('program', 9) }}</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts">
import {
  iconCalendar,
  iconContacts,
  iconEmails,
  iconFiles,
  iconPlace,
  iconProgram,
  iconQuestioning,
  iconSettings,
  iconStudent,
} from '@/icons';
</script>
