<template>
  <full-dialog icon="fact_check" :title="formTitle" :subtitle="subtitle" class="small" hide-drawer>
    <template #page>
      <!-- TODO: control this with a new configurable element at form level, we can use it for addresses, files, etc.-->
      <!--<div v-if="addressesApiEndpoint" class="q-px-lg q-mt-md q-mb-xl">
        <h5 class="text-h6 text-grey-8 text-weight-regular q-mt-none q-mb-md">
          {{ $t('address', 9) }}
        </h5>
        <address-cards :api-endpoint="addressesApiEndpoint" />
      </div>-->
      <marked-div v-if="formDescription" :text="formDescription" class="q-mb-xl q-px-lg" />
      <div v-for="(fieldset, idx) in visibleFieldsets" :key="idx" class="q-px-lg q-mb-lg">
        <h5 v-if="fieldset.legend" class="text-grey-8 text-weight-regular q-mb-lg">
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
            >
              <template #label></template>
            </q-select>
            <div v-else-if="field.type === 'option_group'">
              <q-option-group
                v-model="mutable[field.code]"
                :options="(field.options as TranslatedFieldOption[])"
                :type="field.multiple ? 'checkbox' : 'radio'"
                dense
              />
              <q-input
                v-if="field.other_option && (mutable[field.code] as (number | string)[]).includes(field.other_option)"
                v-model="mutable[`${field.code}__${field.other_option}`]"
                :label="(field.options.find((option) => option.value === field.other_option)?.label as string)"
                type="text"
                filled
                dense
                class="q-ml-lg q-mt-sm"
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
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <q-separator />
      <div class="row q-ma-lg">
        <div class="col-12 col-md text-grey-8 text-caption">
          <div v-if="pendingFields.length && pendingFields.length < 5">
            <span class="bg-yellow-2">{{ $t('form.pending_fields') }}:</span><br />
            <ul>
              <li v-for="field in pendingFields" :key="field" class="ellipsis">{{ field }}</li>
            </ul>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <q-btn
            @click="save"
            unelevated
            color="ugent"
            :label="existingResponse ? $t('form.update') : $t('form.save')"
            :disable="!formIsValid"
            class="float-right"
          />
        </div>
      </div>
    </template>
  </full-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios';
import { notify } from '@/notify';

import MarkedDiv from '../MarkedDiv.vue';
import FullDialog from '../FullDialog.vue';

const { t, locale } = useI18n();

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  questioning: Questioning;
  modelValue: CustomFormResponse[];
  addressesApiEndpoint?: ApiEndpoint;
  subtitle?: string | undefined;
}>();

const processing = ref(false);
const responses = ref<CustomFormResponse[]>(props.modelValue);
const definition = ref<CustomFormDefinition>(props.questioning.form_definition as CustomFormDefinition);
const mutable = ref<CustomFormData>(
  props.modelValue.find((response) => response.questioning === props.questioning.id)?.data || ({} as CustomFormData)
);

const formTitle = computed<string>(() => {
  if (definition.value.title) {
    return locale.value === 'en' ? definition.value.title.en : definition.value.title.nl;
  }
  return 'Form';
});

const formDescription = computed<string | null>(() => {
  if (definition.value.description) {
    return locale.value === 'en' ? definition.value.description.en : definition.value.description.nl;
  }
  return null;
});

const existingResponse = computed<CustomFormResponse | undefined>(() => {
  return responses.value.find((response) => response.questioning === props.questioning.id);
});

const pendingFields = computed<string[]>(() => {
  return (props.questioning.form_definition as CustomFormDefinition).fieldsets.reduce((acc, fieldset) => {
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
      }, [] as string[])
    );
  }, [] as string[]);
});

const formIsValid = computed<boolean>(() => {
  return (props.questioning.form_definition as CustomFormDefinition).fieldsets.every((fieldset) => {
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
  return ['text', 'textarea', 'number', 'date', 'email', 'tel', 'url'].includes(field.type);
}

function getTextValue(translation: Translation): string {
  return translation[locale.value as 'en' | 'nl'] || translation.nl;
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
    (fieldset) => !processing.value && fieldsetIsVisible(fieldset)
  );
});

function save(): void {
  if (existingResponse.value) {
    api
      .put(existingResponse.value.self, { data: mutable.value, questioning: existingResponse.value.questioning })
      .then((res) => {
        const idx = responses.value.findIndex((r) => r.id === res.data.id);
        responses.value[idx] = res.data;
        notify.success(t('form.updated'));
        emit('update:modelValue', responses.value);
      });
  } else {
    api.post(props.apiEndpoint, { data: mutable.value, questioning: props.questioning.id }).then((res) => {
      responses.value.push(res.data);
      notify.success(t('form.saved'));
      emit('update:modelValue', responses.value);
    });
  }
}

watch(
  () => mutable.value,
  () => {
    updateResponseObject();
  },
  { deep: true }
);

const updateResponseObject = () => {
  processing.value = true;
  (props.questioning.form_definition as CustomFormDefinition).fieldsets.forEach((fieldset) => {
    if (!fieldsetIsVisible(fieldset)) {
      fieldset.fields.forEach((field) => {
        if (field.code in mutable.value) {
          delete mutable.value[field.code];
        }
      });
    } else {
      fieldset.fields.forEach((field) => {
        if (!(field.code in mutable.value)) {
          if (field.type === 'option_grid') {
            if (field.multiple) {
              mutable.value[field.code] = [];
            } else {
              mutable.value[field.code] = {};
            }
          } else if ((field.type === 'select' || field.type === 'option_group') && field.multiple) {
            mutable.value[field.code] = [];
            if (field.other_option) {
              mutable.value[`${field.code}__${field.other_option}`] = '';
            }
          } else {
            mutable.value[field.code] = '';
          }
        }
      });
    }
  });
  processing.value = false;
};

updateResponseObject();
</script>
