<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'planning' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="calendar_month" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('allocation') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'students' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="person_search" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('student', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'places' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="business" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('place', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'placeContacts' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="portrait" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('contact', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'questionings' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="task_alt" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('questioning', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'documents' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="drive_file_move_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('document', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'emails' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="mail_outline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('field.email', 9) }}</q-item-section>
        </q-item>
        <q-item-label header>{{ $t('settings') }}</q-item-label>
        <q-item clickable :to="{ name: 'project' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="settings" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('project') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'programs' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="polyline" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('program', 9) }}</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts"></script>
