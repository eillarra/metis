<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm">
        <q-item clickable :to="{ name: 'planning' }">
          <q-item-section avatar>
            <q-icon name="calendar_month" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('planning') }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'students' }">
          <q-item-section avatar>
            <q-icon name="person_search" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('student', 9) }}</q-item-section>
        </q-item>
        <q-separator class="q-my-sm" />
        <q-item clickable :to="{ name: 'places' }">
          <q-item-section avatar>
            <q-icon name="business" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('place', 9) }}</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'placeContacts' }">
          <q-item-section avatar>
            <q-icon name="portrait" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('place_contact', 9) }}</q-item-section>
        </q-item>
        <q-separator class="q-my-sm" />
        <q-item clickable :to="{ name: 'programs' }">
          <q-item-section avatar>
            <q-icon name="app_registration" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('program', 9) }}</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts"></script>
