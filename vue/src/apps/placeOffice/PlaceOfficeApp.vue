<template>
  <div>
    {{ djangoPlace }}
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

const page = usePage();

const djangoPlace = computed<Place>(() => page.props.place as Place);
</script>
