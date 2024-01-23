<template>
  <q-card v-if="place" flat bordered class="q-pa-md">
    <h6 class="q-mt-none q-mb-sm">Stageplaats</h6>
    <strong>{{ place.name }}</strong>
    <div v-for="address in place.addresses" :key="address.id">
      <q-separator class="q-my-md" />
      <q-icon name="map" class="float-right" />
      <span>{{ address.address }}</span><br />
      <span>{{ address.postcode }} {{ address.city }}</span>
    </div>
    <q-separator class="q-my-md" />
    <div v-for="contact in place.contacts" :key="contact.id">
      <q-icon name="person" class="float-right" />
      <span>{{ contact.user.name }}</span><br />
      <span>{{ contact.user.email }}</span><br />
      <span>{{ contact.user.phone_numbers }}</span>
    </div>
  </q-card>
</template>

<script setup lang="ts">
defineProps<{
  place: Place;
}>();
</script>
