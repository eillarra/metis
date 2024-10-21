<template>
  <q-card v-if="place" flat bordered class="q-pa-md">
    <h6 class="q-mt-none q-mb-sm">Stageplaats</h6>
    <strong>{{ place.name }}</strong>
    <div v-for="address in place.addresses" :key="address.id">
      <q-separator class="q-my-md" />
      <q-icon :name="iconMap" class="float-right" />
      <span>{{ address.address }}</span
      ><br />
      <span>{{ address.postcode }} {{ address.city }}</span>
    </div>
  </q-card>
</template>

<script setup lang="ts">
import { iconMap } from '@/icons';

defineProps<{
  place: Place;
}>();
</script>
