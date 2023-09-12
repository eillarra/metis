<template>
  <dialog-form icon="fact_check" :title="formTitle">
    <template #page>
      <div v-if="addressesApiEndpoint" class="q-px-lg q-mt-md q-mb-xl">
        <h5 class="text-h6 text-grey-8 text-weight-regular q-mt-none q-mb-md">
          {{ $t('address', 9) }}
        </h5>
        <address-cards :api-endpoint="addressesApiEndpoint" />
      </div>
      <div v-for="(fieldset, idx) in translatedFormDefinition.fieldsets" :key="idx" class="q-px-lg q-mt-md q-mb-xl">
        <h5 v-if="fieldset.legend" class="text-h6 text-grey-8 text-weight-regular q-mt-none q-mb-md">
          {{ getTextValue(fieldset.legend) }}
        </h5>
        <div class="q-gutter-y-sm">
          <div v-for="field in fieldset.fields" :key="field.code || field.component">
            <q-input
              v-if="isInputField(field)"
              v-model="mutable[field.code]"
              :type="field.type"
              :mask="field.mask || undefined"
              :label="getTextValue(field.label)"
              dense
              filled
            >
              <template v-slot:append v-if="field.required">
                <q-icon name="emergency" size="xs" color="orange" />
              </template>
            </q-input>
            <q-select
              v-else-if="field.type === 'select'"
              v-model="mutable[field.code]"
              :options="field.options"
              :id="field.code"
              :name="field.code"
              :label="getTextValue(field.label)"
              :multiple="field.multiple"
              emit-value
              map-options
              dense
            >
              <template v-slot:append v-if="field.required">
                <q-icon name="emergency" size="xs" color="orange" />
              </template>
            </q-select>
            <div v-else-if="field.type === 'option_group'" class="q-mb-md">
              <q-field dense borderless :label="getTextValue(field.label)" readonly>
                <template v-slot:append v-if="field.required">
                  <q-icon name="emergency" size="xs" color="orange" />
                </template>
              </q-field>
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
              <q-field dense borderless :label="getTextValue(field.label)" readonly>
                <template v-slot:append v-if="field.required">
                  <q-icon name="emergency" size="xs" color="orange" />
                </template>
              </q-field>
              <div v-for="option in field.options" :key="option.value" class="row">
                <div class="col-12 col-sm-6">{{ option.label }}<q-separator v-show="!$q.screen.lt.sm" /></div>
                <div v-for="col in field.columns" :key="col.value" class="col-4 col-sm-2 text-right">
                  <q-checkbox
                    v-model="mutable[field.code]"
                    :label="col.label"
                    :val="`${option.value}_${col.value}`"
                    dense
                    class="q-mr-sm"
                  />
                  <q-separator />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="row q-ma-lg">
        <div v-if="pendingFields.length" class="col-12 col-md text-grey-8">
          <span class="bg-yellow-2">{{ $t('form.pending_fields') }}:</span><br />
          {{ pendingFields.join(', ') }}
        </div>
        <div class="col-12 col-md">
          <q-btn
            @click="save"
            unelevated
            color="ugent"
            :label="existingResponse ? $t('form.update') : $t('form.save')"
            :disable="!formIsValid"
            class="float-right"
          />
          TOOD: kotadress in same place
        </div>
      </div>
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios';
import { notify } from '@/notify';

import DialogForm from '../forms/DialogForm.vue';
import AddressCards from '../rel/AddressCards.vue';

const { t, locale } = useI18n();

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  questioning: Questioning;
  modelValue: CustomFormResponse[];
  addressesApiEndpoint?: ApiEndpoint;
}>();

const responses = ref<CustomFormResponse[]>(props.modelValue);
const definition = ref<CustomFormDefinition>(props.questioning.form_definition);
const mutable = ref<CustomFormData>(
  props.modelValue.find((response) => response.questioning === props.questioning.id)?.data || {}
);

const formTitle = computed<string>(() => {
  if (definition.value.title) {
    return locale.value === 'en' ? definition.value.title.en : definition.value.title.nl;
  }
  return 'Form';
});

const existingResponse = computed<CustomFormResponse | undefined>(() => {
  return responses.value.find((response) => response.questioning === props.questioning.id);
});

const pendingFields = computed<string[]>(() => {
  return props.questioning.form_definition.fieldsets.reduce((acc, fieldset) => {
    return acc.concat(
      fieldset.fields.reduce((acc, field) => {
        if (field.required) {
          if (
            (((field.type === 'select' || field.type === 'option_group') && field.multiple) ||
              field.type === 'option_grid') &&
            !(mutable.value[field.code] as []).length
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

props.questioning.form_definition.fieldsets.forEach((fieldset) => {
  fieldset.fields.forEach((field) => {
    if (!mutable.value[field.code]) {
      if (field.type === 'option_grid') {
        mutable.value[field.code] = [];
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
});

const formIsValid = computed<boolean>(() => {
  return props.questioning.form_definition.fieldsets.every((fieldset) => {
    return fieldset.fields.every((field) => {
      if (field.required) {
        if (
          ((field.type === 'select' || field.type === 'option_group') && field.multiple) ||
          field.type === 'option_grid'
        ) {
          return (mutable.value[field.code] as []).length > 0;
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
      if (field.type === 'option_grid' && field.columns) {
        field.columns = (field.columns as FieldOption[]).map((column) => {
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
</script>
