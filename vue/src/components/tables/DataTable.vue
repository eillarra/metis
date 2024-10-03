<style lang="scss">
$in-table-dense-field-height: 28px;

.ugent__create-btn .q-btn {
  padding: 0 !important;
  min-height: 40px !important;

  &:hover {
    background-color: #e6f0ff !important;
    color: white;
  }
}

.ugent__data-table {
  &.dense {
    .q-field--dense .q-field__control, .q-field--dense .q-field__marginal {
      height: $in-table-dense-field-height;
    }
    .q-field--auto-height.q-field--dense .q-field__control, .q-field--auto-height.q-field--dense .q-field__native {
      min-height: $in-table-dense-field-height;
    }
  }

  .q-table {
    max-width: 100%;

    th, td {
      background-color: white;
      max-width: 300px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    th.sticky-left,
    td.sticky-left {
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

    .q-badge {
      vertical-align: text-bottom;
      padding: 2px 4px 1px;
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
        v-if="!hideColumnSelector"
        v-model="visibleColumns"
        multiple
        dense
        square
        filled
        options-dense
        :display-value="$q.lang.table.columns"
        :options="selectableColumns"
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
      <slot name="selected-action" v-if="selected"></slot>
    </div>
    <q-table
      class="ugent__data-table q-mb-xl"
      flat
      dense
      :rows="queriedRows"
      :columns="extendedColumns"
      :visible-columns="visibleColumns.concat(['edit', 'remove'])"
      :row-key="(row) => row._self.id"
      :loading="loading"
      :hide-pagination="hidePagination"
      :pagination="initialPagination"
      binary-state-sort
      :selection="selection || 'none'"
      v-model:selected="selected"
    >
      <template #header-selection="scope">
        <q-checkbox
          v-model="scope.selected"
          :disable="!selectableAmount"
          size="sm"
          dense
          :color="selectableAmount ? 'grey-8' : 'grey-4'"
          keep-color
        />
      </template>
      <template #body-selection="scope">
        <q-checkbox
          v-model="scope.selected"
          :disable="scope.row._hide_selection"
          size="sm"
          dense
          :color="!scope.row._hide_selection ? 'grey-8' : 'grey-4'"
          keep-color
        />
      </template>
      <template #body-cell="props">
        <!-- Custom boolean field -->
        <q-td
          :props="props"
          :auto-width="
            props.col.name.startsWith('is_') ||
            props.col.name.startsWith('has_') ||
            props.col.name == 'last_login' ||
            props.col.autoWidth
          "
          :class="props.row._class || ''"
        >
          <span v-if="props.col.name.startsWith('is_') || props.col.name.startsWith('has_')">
            <q-icon v-if="props.value" name="check_circle" color="green" :size="iconSize" />
            <q-icon v-else name="block" color="grey" :size="iconSize" />
          </span>
          <span v-else-if="props.col.name.endsWith('_badge')" class="q-gutter-x-xs">
            <q-badge v-if="props.value" outline :label="props.value" color="dark" />
          </span>
          <span v-else-if="props.col.name == 'remarks'">
            <q-icon
              :name="props.value > 0 ? iconChat : 'chat_bubble_outline'"
              :color="props.value > 0 ? 'dark' : 'grey-4'"
              :size="iconSize"
            />
          </span>
          <span v-else-if="props.col.name.startsWith('steps_')" class="q-gutter-x-xs">
            <q-icon v-for="(step, k) in props.value" :key="k" :name="step.icon" :color="step.color" :size="iconSize" />
          </span>
          <span v-else-if="props.col.name == 'disciplines'" class="q-gutter-x-xs">
            <q-badge outline v-for="d in props.value" :key="d.code" :label="d.name" color="dark" />
          </span>
          <span v-else-if="props.col.name.startsWith('check_')" class="q-gutter-x-xs">
            <span>{{ props.value[0] }}</span>
            <q-icon
              :name="props.value[1] == true ? 'check' : 'radio_button_checked'"
              :color="props.value[1] == true ? 'dark' : 'orange-8'"
              :size="iconSize"
              class="q-ml-xs"
            />
          </span>
          <div v-else-if="props.col.name.startsWith('progress_')" class="row full-width items-center">
            <div class="col-9 q-pr-xs">
              <q-linear-progress
                rounded
                :value="props.value / 100"
                :color="props.value < 100 ? 'primary' : 'green'"
                :instant-feedback="false"
              />
            </div>
            <div class="col text-right text-caption">{{ props.value }}%</div>
          </div>
          <span v-else>{{ props.value }}</span>
        </q-td>
      </template>
      <template #body-cell-email="props">
        <!-- Custom email field -->
        <q-td :props="props" auto-width :class="props.row._class || ''">
          <a :href="`mailto:${props.row.email}`" target="_blank" rel="noopener" class="inherit">{{
            props.row.email
          }}</a>
          <i
            @click="copyText(props.row.email)"
            class="q-icon notranslate material-icons cursor-pointer q-ml-xs"
            :style="{ 'font-size': iconSize }"
            aria-hidden="true"
            role="presentation"
            >content_copy</i
          >
        </q-td>
      </template>
      <template #body-cell-remove="props">
        <!-- Remove icon -->
        <q-td :props="props" auto-width :class="props.row._class || ''">
          <q-icon @click="removeRow(props.row)" name="backspace" :size="iconSize" color="red" class="cursor-pointer" />
        </q-td>
      </template>
      <template #body-cell-edit="props">
        <!-- Edit icon -->
        <q-td :props="props" auto-width :class="props.row._class || ''">
          <q-icon
            @click="selectObj(props.row)"
            :name="openDialog ? 'open_in_browser' : 'edit'"
            :size="iconSize"
            color="ugent"
            class="cursor-pointer"
          />
        </q-td>
      </template>
      <template #body-cell-download="props">
        <!-- Download icon -->
        <q-td :props="props" auto-width :class="props.row._class || ''">
          <a :href="props.row.download" target="_blank" rel="noopener" class="inherit">
            <q-icon name="download" :size="iconSize" color="ugent" class="cursor-pointer" />
          </a>
        </q-td>
      </template>
    </q-table>
    <q-dialog v-if="formComponent" v-model="dialogVisible" position="bottom">
      <component :is="formComponent" :obj="selectedObj" @delete:obj="() => (selectedObj = null)" />
    </q-dialog>
    <q-dialog v-if="createFormComponent" v-model="createDialogVisible">
      <component :is="createFormComponent" @create:obj="() => (createDialogVisible = false)" />
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch, ComponentOptions, getCurrentInstance } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { copyToClipboard } from 'quasar';
import { cloneDeep } from 'lodash-es';
import { Md5 } from 'ts-md5';

import { notify } from '@/notify';
import { storage } from '@/storage';

import { iconChat } from '@/icons';

const emit = defineEmits(['update:selected', 'remove:row']);

const router = useRouter();
const route = useRoute();
const { t } = useI18n();

const props = defineProps<{
  columns: object[];
  rows: QuasarTableRow[];
  rowsPerPage?: number;
  queryColumns?: string[];
  hiddenColumns?: string[];
  formComponent?: ComponentOptions | undefined;
  createFormComponent?: ComponentOptions | undefined;
  sortBy?: string;
  loading?: boolean;
  hideToolbar?: boolean;
  hideColumnSelector?: boolean;
  hidePagination?: boolean;
  inDialog?: boolean;
  selection?: 'multiple' | 'single' | 'none';
  selected?: QuasarTableRow[];
  openDialog?: boolean /* TODO: this can be solved in another way, as it is only for custom open icon */;
  removable?: boolean;
}>();

const openDialog = ref<boolean>(props.openDialog || false);
const selected = ref<QuasarTableRow[]>(props.selected || []);
const selectableAmount = computed<number>(() => props.rows.filter((r) => !r._hide_selection).length);

const initialPagination = {
  rowsPerPage: props.rowsPerPage || 25,
  sortBy: props.sortBy?.replace('-', '') || undefined,
  descending: props.sortBy?.startsWith('-') || false,
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

  // add custom remove field
  if (props.removable) {
    columns.push({
      name: 'remove',
      label: null,
      field: 'remove',
      align: 'center',
      headerClasses: 'sticky-right',
      classes: 'sticky-right',
    });
  }

  return columns;
});

const selectableColumns = computed(() => props.columns.filter((c) => c.label));

const parentName = getCurrentInstance()?.parent?.type.__name || '';
const fullPath = `${window.location.href.split('#')[0]}#${route.path}&component=${parentName}`;
const queryStorageKey = Md5.hashStr(`data_table.query.${fullPath}`);
const query = ref<string>(props.hideToolbar ? '' : storage.get(queryStorageKey) || route.query.q?.toString() || '');
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

const visibleColumnsStorageKey = Md5.hashStr(`data_table.visible_columns.${fullPath}`);
const visibleColumns = ref<string[]>(props.hideToolbar ? [] : storage.get(visibleColumnsStorageKey) || []);

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

function removeRow(row: object) {
  emit('remove:row', row);
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
  if (props.inDialog) return;
  router.push({ query: { q: newVal || undefined } });
  storage.set(queryStorageKey, newVal);
});

watch(visibleColumns, (newVal) => {
  storage.set(visibleColumnsStorageKey, newVal);
});

if (!props.hideToolbar && storage.get(queryStorageKey)) {
  router.push({ query: { q: storage.get(queryStorageKey) } });
}

watch(selected, (val) => {
  if (!val) return;
  if (val.length !== props.selected?.length) {
    emit('update:selected', val);
  }
});

// watch if props.selected is emptied or filled

watch(
  () => props.selected,
  (val) => {
    if (!val || (val.length === 0 && selected.value.length > 0)) {
      selected.value = [];
    } else {
      selected.value = val.filter((obj) => !obj._hide_selection);
    }
  }
);
</script>
