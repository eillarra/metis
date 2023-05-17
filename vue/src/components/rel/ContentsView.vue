<template>
  <div v-if="loading" class="flex flex-center q-mt-xl">
    <q-spinner color="grey-3" size="4em" />
  </div>
  <div v-else>CONTENTS VIEW</div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { usePage } from '@inertiajs/vue3';

import { api } from '@/axios';

const page = usePage();

const props = defineProps<{
  apiEndpoints: Record<string, ApiEndpoint> | null;
  remarkTypes?: Record<string, string>;
}>();

const loading = ref<boolean>(false);
const remarks = ref<Remark[]>([]);

async function fetchContents() {
  if (!props.apiEndpoints) return;
  for (const [key, endpoint] of Object.entries(props.apiEndpoints)) {
    const { data } = await api.get<Remark[]>(endpoint);
    remarks.value.push(...data.map((remark) => ({ ...remark, type: key })));
  }
  loading.value = false;
}

fetchContents();

watch(() => props.apiEndpoints, fetchContents);
</script>
