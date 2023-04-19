<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm">
        <q-item clickable :to="{ name: 'programs' }">
          <q-item-section avatar>
            <q-icon name="app_registration" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Programs</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'students' }">
          <q-item-section avatar>
            <q-icon name="person_search" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Students</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'calendar' }">
          <q-item-section avatar>
            <q-icon name="calendar_month" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Calendar</q-item-section>
        </q-item>
        <q-item clickable :to="{ name: 'places' }">
          <q-item-section avatar>
            <q-icon name="business" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>Places</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts"></script>
