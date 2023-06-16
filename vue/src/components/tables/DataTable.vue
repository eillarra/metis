<style lang="scss">
.ugent__create-btn .q-btn {
  padding: 0 !important;
  min-height: 40px !important;

  .q-icon {
    font-size: 1em;
    margin-right: 0.25em;
    width: 0.75em;
  }

  &:hover {
    background-color: #e6f0ff !important;
    color: white;
  }
}

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
      background-color: white;
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
  <div>
    <div v-if="!hideToolbar" class="row q-col-gutter-sm q-mb-lg">
      <q-input v-if="queryColumns" v-model="query" clearable dense square filled type="text" class="col-12 col-md">
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>
      <q-select
        v-model="visibleColumns"
        multiple
        dense
        square
        filled
        options-dense
        :display-value="$q.lang.table.columns"
        :options="columns"
        option-disable="required"
        option-value="name"
        option-label="label"
        class="col col-md-2"
        emit-value
        map-options
      >
        <template #prepend>
          <q-icon name="view_column" />
        </template>
      </q-select>
      <div v-if="createFormComponent" class="col-6 col-md-1 ugent__create-btn">
        <q-btn
          unelevated
          color="blue-1"
          :label="$t('form.new')"
          icon="add"
          class="text-ugent full-width"
          @click="createDialogVisible = true"
        />
      </div>
    </div>
    <q-table
      class="ugent__data-table q-mb-xl"
      flat
      dense
      :rows="queriedRows"
      :columns="extendedColumns"
      :visible-columns="visibleColumns.concat(['edit'])"
      row-key="_self.id"
      :loading="loading"
      :hide-pagination="hidePagination"
      :pagination="initialPagination"
      binary-state-sort
    >
      <template #body-cell="props">
        <!-- Custom boolean field -->
        <q-td
          :props="props"
          :auto-width="
            props.col.name.startsWith('is_') || props.col.name.startsWith('has_') || props.col.name == 'last_login'
          "
          :class="props.row._class || ''"
        >
          <span v-if="props.col.name.startsWith('is_') || props.col.name.startsWith('has_')">
            <q-icon v-if="props.value" name="check_circle" color="green" :size="iconSize" />
            <q-icon v-else name="block" color="grey" :size="iconSize" />
          </span>
          <span v-else-if="props.col.name == 'disciplines'" class="q-gutter-x-xs">
            <q-badge outline v-for="d in props.value" :key="d.code" :label="d.name" color="dark" />
          </span>
          <span v-else>{{ props.value }}</span>
        </q-td>
      </template>
      <template #body-cell-email="props">
        <!-- Custom email field -->
        <q-td :props="props" auto-width>
          <a :href="`mailto:${props.row.email}`" target="_blank" rel="noopener" class="inherit">{{
            props.row.email
          }}</a>
          <q-icon
            @click="copyText(props.row.email)"
            name="content_copy"
            :size="iconSize"
            class="cursor-pointer q-ml-xs"
          />
        </q-td>
      </template>
      <template #body-cell-edit="props">
        <!-- Edit icon -->
        <q-td :props="props" auto-width>
          <q-icon @click="selectObj(props.row)" name="edit" :size="iconSize" color="ugent" class="cursor-pointer" />
        </q-td>
      </template>
    </q-table>
    <q-dialog v-if="formComponent" v-model="dialogVisible">
      <component :is="formComponent" :obj="selectedObj" @delete:obj="() => (selectedObj = null)" />
    </q-dialog>
    <q-dialog v-if="createFormComponent" v-model="createDialogVisible">
      <component :is="createFormComponent" @create:obj="() => (createDialogVisible = false)" />
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch, ComponentOptions } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { copyToClipboard } from 'quasar';
import { cloneDeep } from 'lodash-es';

import { notify } from '@/notify';
import { storage } from '@/storage';

const router = useRouter();
const route = useRoute();
const { t } = useI18n();

const props = defineProps<{
  columns: object[];
  rows: object[];
  queryColumns?: string[];
  hiddenColumns?: string[];
  formComponent?: ComponentOptions;
  createFormComponent?: ComponentOptions;
  sortBy?: string;
  loading?: boolean;
  hideToolbar?: boolean;
  hidePagination?: boolean;
}>();

const initialPagination = {
  rowsPerPage: 25,
  sortBy: props.sortBy || undefined,
};

const iconSize = '16px';

const extendedColumns = computed(() => {
  const columns = [...props.columns];

  // add custom edit field
  if (props.formComponent) {
    columns.push({
      name: 'edit',
      label: null,
      field: 'edit',
      align: 'center',
      headerClasses: 'sticky-right',
      classes: 'sticky-right',
    });
  }

  return columns;
});

const queryStorageKey = computed<string>(() => `metis.data_table.query.${route.name?.toString()}`);
const query = ref<string>(storage.get(queryStorageKey.value) || route.query.q?.toString() || '');
const queriedRows = computed(() => {
  if (!query.value || !props.queryColumns) {
    return props.rows;
  }

  // we split the query search and count the matches
  // if the number of matches is equal to the number of query terms, we have a match

  const queryTerms = query.value.toLowerCase().split(' ');

  return props.rows.filter((row) => {
    let matches = 0;

    for (const queryTerm of queryTerms) {
      for (const column of props.queryColumns as string[]) {
        if (row[column]?.toLowerCase().includes(queryTerm)) {
          matches++;
          break;
        }
      }
    }
    return matches === queryTerms.length;
  });
});

const visibleColumnsStorageKey = computed<string>(() => `metis.data_table.visible_columns.${route.name?.toString()}`);
const visibleColumns = ref<string[]>(storage.get(visibleColumnsStorageKey.value) || []);

const createDialogVisible = ref<boolean>(false);
const selectedObj = ref<object | null>(null);
const dialogVisible = computed<boolean>({
  get() {
    return !!selectedObj.value;
  },
  set(value) {
    if (!value) {
      selectedObj.value = null;
    }
  },
});

function copyText(text: string) {
  copyToClipboard(text).then(() => {
    notify.info(t('copied_to_clipboard'));
  });
}

function selectObj(row: { _self: object }) {
  selectedObj.value = cloneDeep(row._self);
}

onMounted(() => {
  if (visibleColumns.value.length === 0) {
    visibleColumns.value = props.columns.filter((c) => !props.hiddenColumns?.includes(c.name)).map((c) => c.name);
  }
});

watch(query, (newVal) => {
  router.push({ query: { q: newVal || undefined } });
  storage.set(queryStorageKey.value, newVal);
});

watch(visibleColumns, (newVal) => {
  storage.set(visibleColumnsStorageKey.value, newVal);
  // TODO: save to user's preferences via API
});

if (storage.get(queryStorageKey.value)) {
  router.push({ query: { q: storage.get(queryStorageKey.value) } });
}
</script>
