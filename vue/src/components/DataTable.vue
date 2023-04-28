<style lang="scss">
.ugent__data-table {
  .q-table {
    max-width: 100%;

    th.sticky-left,
    td.sticky-left {
      background-color: white;
      position: -webkit-sticky;
      position: sticky;
      left: 0;
      z-index: 1;
    }

    th.sticky-right,
    td.sticky-right {
      position: -webkit-sticky;
      position: sticky;
      right: 0;
      z-index: 2;
    }
  }

  .q-field,
  thead th,
  tbody td {
    font-size: 1em;
  }

  thead th {
    font-family: 'UGent Panno Medium', 'Arial', sans-serif;
  }

  .q-table__bottom {
    font-size: smaller;
  }
}
</style>

<template>
  <div class="row q-col-gutter-sm q-mb-lg">
    <h3 class="text-ugent col-12 col-md-3 q-mb-none">{{ props.title }}</h3>
    <q-input dense square filled type="text" v-model="query" class="col-12 col-md">
      <template #prepend>
        <q-icon name="search" />
      </template>
      <template #append>
        <q-icon v-if="query !== ''" name="close" @click="query = ''" class="cursor-pointer" />
      </template>
    </q-input>
    <slot name="filters" />
    <q-select
      v-model="visibleColumns"
      multiple
      outlined
      dense
      square
      options-dense
      :display-value="$q.lang.table.columns"
      :options="columns"
      option-disable="required"
      option-value="name"
      option-label="label"
      class="col-12 col-md-2"
      emit-value
      map-options
    >
      <template #prepend>
        <q-icon name="view_column" />
      </template>
    </q-select>
  </div>
  <q-table
    class="ugent__data-table q-mb-xl"
    flat
    dense
    :rows="queriedRows"
    :columns="columns"
    row-key="name"
    :visible-columns="visibleColumns"
    :loading="loading"
    :pagination="initialPagination"
    binary-state-sort
  >
    <template #body-cell-email="props">
      <q-td :props="props" auto-width>
        <a href="mailto:props.row.email" target="_blank" rel="noopener" class="inherit">{{ props.row.email }}</a>
        <q-icon @click="copyText(props.row.email)" name="content_copy" size="13px" class="cursor-pointer q-ml-xs" />
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch, ComputedRef, Ref } from 'vue';
import { useRouter } from 'vue-router';
import { copyToClipboard, Notify } from 'quasar';

import { storage } from '@/storage';

const router = useRouter();

const props = defineProps<{
  title: string;
  loading: boolean;
  rows: any[];
  columns: any[];
  queryColumns: string[];
  sortBy?: string;
}>();

const initialPagination = {
  rowsPerPage: 25,
  sortBy: props.sortBy || null,
};

const query = ref('');

const queriedRows = computed(() => {
  if (!query.value) {
    return props.rows;
  }

  // we split the query search and count the matches
  // if the number of matches is equal to the number of query terms, we have a match

  const queryTerms = query.value.toLowerCase().split(' ');

  return props.rows.filter((row) => {
    let matches = 0;

    for (const queryTerm of queryTerms) {
      for (const column of props.queryColumns) {
        if (row[column]?.toLowerCase().includes(queryTerm)) {
          matches++;
          break;
        }
      }
    }
    return matches === queryTerms.length;
  });
});

const visibleColumnsStorageKey: ComputedRef<string> = computed(
  () => `metis.data_table.visible_columns.${router.currentRoute.value.name}`
);
const visibleColumns: Ref<string[]> = ref(storage.get(visibleColumnsStorageKey.value) || []);

function copyText(text: string) {
  copyToClipboard(text).then(() => {
    Notify.create({
      message: 'Copied to clipboard',
      color: 'positive',
      icon: 'check',
    });
  });
}

onMounted(() => {
  if (visibleColumns.value.length === 0) {
    visibleColumns.value = props.columns.map((column) => column.name);
  }
});

/*
deep watch visibleColumns and save user's selection in local storage
*/
watch(visibleColumns, (newVal) => {
  // TODO: save to user's preferences via API
  storage.set(visibleColumnsStorageKey.value, newVal);
});
</script>
