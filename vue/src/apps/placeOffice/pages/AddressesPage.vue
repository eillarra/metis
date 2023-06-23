<template>
  <div class="q-mb-xl">
    <h3 class="text-ugent col-12 col-md-3 q-mb-lg">{{ $t('address', 9) }}</h3>
    <address-cards :api-endpoint="(place?.rel_addresses as ApiEndpoint)" :limit="1" />
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useStore } from '../store.js';

import AddressCards from '@/components/rel/AddressCards.vue';

const { place } = storeToRefs(useStore());
</script>
