<template>
  <div>
    <marked-div v-if="formDescription" :text="formDescription" class="q-mb-xl" />
    <div v-for="(fieldset, idx) in visibleFieldsets" :key="idx" class="q-mb-lg">
      <h5 v-if="fieldset.legend" class="text-body1 text-weight-regular q-mb-lg">
        {{ getTextValue(fieldset.legend) }}
      </h5>
      <div class="q-gutter-y-sm">
        <div v-for="field in fieldset.fields" :key="field.code || field.component" class="q-pb-md">
          <p class="text-body1">
            <q-badge v-if="field.required" color="orange" class="q-mt-xs q-ml-sm float-right">{{
              $t('form.required')
            }}</q-badge>
            <span>{{ getTextValue(field.label) }}</span>
          </p>
          <q-input
            v-if="isInputField(field)"
            v-model="mutable[field.code]"
            :type="field.type"
            :mask="field.mask || undefined"
            :dense="field.type != 'textarea'"
            :disable="props.disable"
            filled
          >
            <template #label></template>
            <template #append v-if="field.required">
              <q-icon name="emergency" size="xs" color="orange" />
            </template>
          </q-input>
          <q-select
            v-else-if="field.type === 'select'"
            v-model="mutable[field.code]"
            :options="field.options"
            :id="field.code"
            :name="field.code"
            :multiple="field.multiple"
            emit-value
            map-options
            dense
            options-dense
          >
            <template #label></template>
          </q-select>
          <div v-else-if="field.type === 'option_group'">
            <q-option-group
              v-model="mutable[field.code]"
              :options="field.options as TranslatedFieldOption[]"
              :type="field.multiple ? 'checkbox' : 'radio'"
              dense
            />
            <q-input
              v-if="field.other_option && (mutable[field.code] as (number | string)[]).includes(field.other_option)"
              v-model="mutable[`${field.code}__${field.other_option}`]"
              :label="
                field.other_label.nl ||
                (field.options.find((option) => option.value === field.other_option)?.label as string)
              "
              type="text"
              filled
              dense
              class="q-ml-lg q-mt-sm"
              :disable="props.disable"
            />
          </div>
          <div v-else-if="field.type === 'option_grid'">
            <div v-for="row in field.rows" :key="row.value" class="row text-body2 items-center">
              <div class="col-12 col-sm-6">{{ row.label }}</div>
              <div v-for="col in field.options" :key="col.value" class="col text-right">
                <q-checkbox
                  v-if="field.multiple"
                  v-model="mutable[field.code]"
                  :label="col.label"
                  :val="`${row.value}_${col.value}`"
                  dense
                  class="q-mr-sm"
                />
                <q-radio
                  v-else
                  v-model="mutable[field.code][row.value]"
                  :label="col.label"
                  :val="col.value"
                  dense
                  class="q-mr-sm"
                />
              </div>
              <div class="col-12 q-py-xs"><q-separator v-show="!$q.screen.lt.sm" /></div>
            </div>
          </div>
          <q-markup-table v-else-if="field.type === 'composite'" flat dense class="ugent__data-table dense">
            <thead class="text-left">
              <tr v-if="(mutable[field.code] || []).length">
                <th v-for="f in field.fields" :key="f.code">
                  {{ getTextValue(f.label) }}
                </th>
                <th v-if="!props.disable"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(_, idx) in mutable[field.code] || []" :key="idx">
                <td v-for="f in field.fields" :key="f.code">
                  <q-input
                    v-if="isInputField(f)"
                    borderless
                    dense
                    v-model="mutable[field.code][idx][f.code]"
                    :type="f.type"
                    :mask="f.mask || undefined"
                    :disable="props.disable"
                    :step="f.type == 'time' ? 3600 : undefined"
                    input-class="q-pa-none ellipsis"
                  />
                  <q-select
                    v-else-if="f.type === 'select'"
                    borderless
                    dense
                    v-model="mutable[field.code][idx][f.code]"
                    :options="f.options"
                    :id="f.code"
                    :name="f.code"
                    :multiple="f.multiple"
                    :disable="props.disable"
                    emit-value
                    map-options
                    options-dense
                    class="ellipsis"
                  />
                </td>
                <td v-if="!props.disable">
                  <q-icon
                    @click="mutable[field.code].splice(idx, 1)"
                    :name="iconDelete"
                    :size="iconSize"
                    color="red"
                    class="cursor-pointer"
                  />
                </td>
              </tr>
            </tbody>
            <tfoot>
              <q-btn
                @click="pushToCompositeField(field)"
                outline
                color="grey-8"
                :label="$t('form.new')"
                class="q-mt-md"
              ></q-btn>
            </tfoot>
          </q-markup-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { cloneDeep } from 'lodash-es';

import MarkedDiv from '../MarkedDiv.vue';

import { iconDelete } from '@/icons';

const { locale } = useI18n();

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  formDefinition: CustomFormDefinition;
  modelValue: CustomFormData;
  subtitle?: string | undefined;
  disable?: boolean | undefined;
}>();

const processing = ref(false);
const definition = ref<CustomFormDefinition>(props.formDefinition as CustomFormDefinition);
const mutable = ref<CustomFormData>(props.modelValue as CustomFormData);
const iconSize = '16px';

const formDescription = computed<string | null>(() => {
  if (definition.value.description) {
    return locale.value === 'en' ? definition.value.description.en : definition.value.description.nl;
  }
  return null;
});

const pendingFields = computed<string[]>(() => {
  return (props.formDefinition as CustomFormDefinition).fieldsets.reduce((acc, fieldset) => {
    if (!fieldsetIsVisible(fieldset)) {
      return acc.concat([]);
    }

    return acc.concat(
      fieldset.fields.reduce((acc, field) => {
        if (field.required) {
          if (
            (field.type === 'select' || field.type === 'option_group' || field.type === 'option_grid') &&
            field.multiple &&
            !(mutable.value[field.code] as []).length
          ) {
          } else if (
            field.type === 'option_grid' &&
            !field.multiple &&
            Object.keys(mutable.value[field.code] as BaseCustomFormData).length < field.rows.length
          ) {
            acc.push(getTextValue(field.label));
          } else if (!mutable.value[field.code]) {
            acc.push(getTextValue(field.label));
          }
        }
        return acc;
      }, [] as string[]),
    );
  }, [] as string[]);
});

const formIsValid = computed<boolean>(() => {
  return (props.formDefinition as CustomFormDefinition).fieldsets.every((fieldset) => {
    if (!fieldsetIsVisible(fieldset)) {
      return true;
    }

    return fieldset.fields.every((field) => {
      if (field.required) {
        if (
          (field.type === 'select' || field.type === 'option_group' || field.type === 'option_grid') &&
          field.multiple
        ) {
          return (mutable.value[field.code] as []).length > 0;
        } else if (field.type === 'option_grid' && !field.multiple) {
          return Object.keys(mutable.value[field.code] as BaseCustomFormData).length == field.rows.length;
        } else {
          return mutable.value[field.code] !== '';
        }
      }
      return true;
    });
  });
});

function isInputField(field: InputField | ChoiceField | GridField): field is InputField {
  return ['text', 'textarea', 'number', 'date', 'time', 'email', 'tel', 'url'].includes(field.type);
}

function getTextValue(translation: Translation): string {
  return translation[locale.value as 'en' | 'nl'] || translation.nl;
}

function pushToCompositeField(field: CompositeField): void {
  /* create a new object if the array exists, otherwise create an array with a single object */
  mutable.value[field.code] = field.code in mutable.value ? [...mutable.value[field.code], {}] : [{}];
}

const translatedFormDefinition = computed<CustomFormDefinition>(() => {
  const formDefinition = cloneDeep(definition.value);

  formDefinition.fieldsets.forEach((fieldset) => {
    fieldset.fields.forEach((field) => {
      if (['select', 'option_group', 'option_grid'].includes(field.type) && field.options) {
        field.options = (field.options as FieldOption[]).map((option) => {
          return {
            ...option,
            label: locale.value === 'en' ? option.label.en : option.label.nl,
          };
        }) as TranslatedFieldOption[];
      }
      if (field.type === 'composite' && field.fields) {
        field.fields.forEach((f) => {
          if (['select'].includes(f.type) && f.options) {
            f.options = (f.options as FieldOption[]).map((option) => {
              return {
                ...option,
                label: locale.value === 'en' ? option.label.en : option.label.nl,
              };
            }) as TranslatedFieldOption[];
          }
        });
      }
      if (field.type === 'option_grid' && field.rows) {
        field.rows = (field.rows as FieldOption[]).map((column) => {
          return {
            ...column,
            label: locale.value === 'en' ? column.label.en : column.label.nl,
          };
        }) as TranslatedFieldOption[];
      }
    });
  });

  return formDefinition;
});

function fieldsetIsVisible(fieldset: Fieldset): boolean {
  if (fieldset.rule) {
    if (fieldset.rule.type === 'equals') {
      return mutable.value[fieldset.rule.field] === fieldset.rule.value;
    }
  }
  return true;
}

const visibleFieldsets = computed<Fieldset[]>(() => {
  return translatedFormDefinition.value.fieldsets.filter(
    (fieldset) => !processing.value && fieldsetIsVisible(fieldset),
  );
});

watch(
  () => props.modelValue,
  (value) => {
    mutable.value = value as CustomFormData;
  },
);
</script>
