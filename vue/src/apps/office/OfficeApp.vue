<template>
  <div>
    {{ education.short_name }}
    {{ $page.props }}
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

const page = usePage();

const education = computed(() => page.props.education);
</script>
