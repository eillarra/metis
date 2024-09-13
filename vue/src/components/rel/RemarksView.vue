<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h4 class="col-12 col-md-3 q-mt-none q-mb-none">
      {{ $t('remark', 9) }}
    </h4>
  </div>
  <div v-if="loading" class="flex flex-center q-mt-xl">
    <q-spinner color="grey-3" size="4em" />
  </div>
  <div v-else>
    <div class="row justify-center">
      <div style="width: 100%">
        <q-chat-message
          v-for="remark in sortedRemarks"
          :key="remark.id"
          :name="remark.updated_by.name"
          :stamp="remark.stamp"
          :bg-color="remark.is_mine ? 'blue-1' : 'grey-2'"
        >
          <div>
            <q-icon
              v-if="remark.is_mine"
              @click="deleteRemark(remark)"
              :name="iconDelete"
              color="red"
              size="20px"
              class="float-right cursor-pointer q-ml-md"
            />
            {{ remark.text }}
          </div>
        </q-chat-message>
      </div>
    </div>
    <div class="bg-white q-pa-lg">
      <!--<q-select
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
      </q-select>-->
      <q-page-sticky expand position="bottom" class="bg-white z-top">
        <div class="full-width full-height text-right q-px-lg q-pb-lg">
          <q-input v-model="remarkText" :label="$t('form.remark.create.new')" autogrow clearable class="q-mb-md" />
          <q-btn @click="addRemark" unelevated color="ugent" :label="$t('form.save')" :disable="remarkText == ''" />
        </div>
      </q-page-sticky>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { usePage } from '@inertiajs/vue3';

import { api } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';
import { formatDate } from '@/utils/dates';

import { iconDelete } from '@/icons';

const { t } = useI18n();

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
    .sort((a, b) => b.updated_at.localeCompare(a.updated_at))
    .map((obj) => ({
      ...obj,
      is_mine: obj.updated_by?.id == djangoUser.value.id,
      stamp: formatDate(obj.updated_at),
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

  api
    .post<Remark>(selectedRemarkEndpoint.value, {
      text: remarkText.value,
    })
    .then(({ data }) => {
      remarks.value.push({ ...data, type: skipTypes.value ? 'default' : selectedRemarkType.value });
      remarkText.value = '';
      notify.success(t('form.remark.create.success'));
    });
}

async function deleteRemark(remark: Remark) {
  confirm(t('form.remark.confirm_delete'), () => {
    api.delete(remark.self).then(() => {
      notify.success(t('form.remark.deleted'));
      remarks.value.splice(remarks.value.indexOf(remark), 1);
    });
  });
}

fetchRemarks();

watch(() => props.apiEndpoints, fetchRemarks);
</script>
