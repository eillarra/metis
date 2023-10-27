<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ $t('document', 9) }}</h3>
    <div class="col"></div>
  </div>
  <ul>
    <li v-if="stagegids">STAGEGIDS: <a :href="stagegids.url" target="_blank">Stagegids</a></li>
  </ul>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

const page = usePage();

const stagegids = computed<File>(() => page.props.files.find((file: File) => file.code === 'stagegids'));
</script>
