<template>
  <q-scroll-area class="fit">
    <div class="q-pb-xl q-pr-md">
      <q-list :dense="$q.screen.gt.sm" class="q-mt-xs">
        <q-item-label header>{{ $t('internship', 9) }}</q-item-label>
        <q-item clickable :to="{ name: 'students' }" active-class="bg-ugent text-white">
          <q-item-section avatar>
            <q-icon name="person_search" size="xs"></q-icon>
          </q-item-section>
          <q-item-section>{{ $t('student', 9) }}</q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts"></script>
