<template>
  <q-select
    v-model="selection"
    dense
    :options="options"
    option-value="id"
    option-label="name"
    :label="$q.lang.label.search"
    :hint="hint"
    input-debounce="250"
    use-input
    hide-selected
    fill-input
    @filter="search"
    :multiple="multiple"
    :clearable="clearable"
  >
    <template #no-option>
      <q-item>
        <q-item-section class="text-grey">{{ $q.lang.table.noResults }}</q-item-section>
      </q-item>
    </template>
    <template #option="scope">
      <q-item v-bind="scope.itemProps">
        <q-item-section>
          <q-item-label>{{ scope.opt.name }}</q-item-label>
          <q-item-label caption>{{ scope.opt.caption }}</q-item-label>
        </q-item-section>
        <q-item section side v-if="scope.opt.disable">
          <q-icon name="check_circle" />
        </q-item>
      </q-item>
    </template>
  </q-select>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

import { api } from '@/axios';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  modelValue: object | null;
  searchEndpoint: ApiEndpoint;
  mapper: (data: ApiObject[]) => QuasarAutocompleteOption[];
  hint?: string;
  clearable?: boolean;
  multiple?: boolean;
}>();

const selection = ref(props.modelValue);
const options = ref<QuasarAutocompleteOption[]>([]);

function search(q: string, update: (arg: () => void) => void, abort: () => void) {
  if (q == '' || q.length < 3) {
    options.value = [];
    abort();
    return;
  }

  api.get(`${props.searchEndpoint}?search=${q}`).then(function (res) {
    update(function () {
      options.value = props.mapper('results' in res.data ? res.data.results : res.data);
    });
  });
}

watch(selection, function (obj) {
  emit('update:modelValue', obj);
});

watch(
  () => props.modelValue,
  function (obj) {
    selection.value = obj;
  }
);
</script>
