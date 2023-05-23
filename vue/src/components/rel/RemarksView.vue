<template>
  <div v-if="loading" class="flex flex-center q-mt-xl">
    <q-spinner color="grey-3" size="4em" />
  </div>
  <div v-else>
    <div class="row">
      <q-input type="text" label="search" class="col-6 col-md-8"></q-input>
      <date-range-filter v-if="remarks.length > 1" v-model="selectedDateRange" class="col-6 col-md-4" />
    </div>
    <q-markup-table flat dense separator="horizontal">
      <tbody>
        <tr v-for="remark in sortedRemarks" :key="remark.id">
          <td>
            <span>{{ remark.text }}</span
            ><br />
            <span class="text-caption">{{ remark.type }}</span>
          </td>
          <td>
            <q-btn v-if="remark.is_mine" @click="deleteRemark(remark)" label="DEL"></q-btn>
          </td>
        </tr>
      </tbody>
    </q-markup-table>
    <div class="fixed-bottom bg-white q-pa-lg">
      <q-separator />
      <q-input v-model="remarkText" filled type="textarea" clearable class="text-body1 q-mb-md" />
      <q-select
        v-if="!skipTypes"
        v-model="selectedRemarkType"
        clearable
        dense
        rounded
        outlined
        :options="remarkTypeOptions"
        :label="$t('type')"
        options-dense
        emit-value
        map-options
        class="col-6 col-md-4"
        :bg-color="selectedRemarkType !== null ? 'blue-1' : 'white'"
      >
        <template #selected-item="scope">
          <span class="ellipsis">{{ scope.opt.label }}</span>
        </template>
      </q-select>
      <div class="q-gutter-md q-mt-md">
        <q-btn @click="addRemark" unelevated color="ugent" label="Add remark" :disable="remarkText == ''" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { usePage } from '@inertiajs/vue3';

import { api } from '@/axios';

import DateRangeFilter from '@/components/DateRangeFilter.vue';

const page = usePage();
const djangoUser = computed<DjangoAuthenticatedUser>(() => page.props.django_user as DjangoAuthenticatedUser);

const props = defineProps<{
  apiEndpoints: Record<string, ApiEndpoint> | null;
  remarkTypes?: Record<string, string>;
}>();

const loading = ref<boolean>(true);
const remarks = ref<Remark[]>([]);
const remarkText = ref<string>('');
const selectedRemarkType = ref<string | null>(null);
const selectedDateRange = ref<QuasarDateRange | null>(null);

const skipTypes = computed(() => {
  // skip type selection if we only have one "default" endpoint
  const keys = Object.keys(props.apiEndpoints ?? {});
  return keys.length == 1 && keys[0] == 'default';
});

const remarkTypeOptions = computed(() => {
  if (!props.apiEndpoints) return [];
  return Object.keys(props.apiEndpoints).map((key) => ({
    label: props.remarkTypes?.[key] ?? key,
    value: key,
  }));
});

const selectedRemarkEndpoint = computed(() => {
  if (skipTypes.value) return props.apiEndpoints?.default;
  if (!props.apiEndpoints) return null;
  return props.apiEndpoints[selectedRemarkType.value];
});

const sortedRemarks = computed<Remark[]>(() => {
  let mutable = [...remarks.value];
  return mutable
    .sort((a, b) => a.updated_at.localeCompare(b.updated_at))
    .map((obj) => ({
      ...obj,
      is_mine: obj.updated_by?.id == djangoUser.value.id,
    }));
});

async function fetchRemarks() {
  if (!props.apiEndpoints) return;
  for (const [key, endpoint] of Object.entries(props.apiEndpoints)) {
    const { data } = await api.get<Remark[]>(endpoint);
    remarks.value.push(...data.map((remark) => ({ ...remark, type: key })));
  }
  loading.value = false;
}

async function addRemark() {
  if (!selectedRemarkEndpoint.value || !remarkText.value) return;
  const { data } = await api.post<Remark>(selectedRemarkEndpoint.value, {
    text: remarkText.value,
  });
  remarks.value.push({ ...data, type: skipTypes.value ? 'default' : selectedRemarkType.value });
  remarkText.value = '';
}

async function deleteRemark(remark: Remark) {
  await api.delete(remark.self);
  remarks.value.splice(remarks.value.indexOf(remark), 1);
}

fetchRemarks();

watch(() => props.apiEndpoints, fetchRemarks);
</script>
