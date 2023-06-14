<template>
  <dialog-form title="" icon="list_alt">
    <template #page>
      <div v-for="(fieldset, idx) in translatedFormDefinition.fieldsets" :key="idx" class="q-px-lg q-mb-xl">
        <h5 v-if="fieldset.legend" class="text-h6 text-grey-8 text-weight-regular q-mt-none q-mb-lg">
          {{ getTextValue(fieldset.legend) }}
        </h5>
        <div class="q-gutter-y-sm">
          <div v-for="field in fieldset.fields" :key="field.code">
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
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <q-btn
        @click="save"
        unelevated
        color="ugent"
        :label="existingResponse ? $t('form.update') : $t('form.save')"
        :disable="!formIsValid"
        class="float-right q-ma-lg"
      />
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios';

import DialogForm from './DialogForm.vue';

const { locale } = useI18n();

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  form: CustomForm;
  modelValue: CustomFormResponse[];
}>();

const responses = ref<CustomFormResponse[]>(props.modelValue);
const definition = ref<CustomFormDefinition>(props.form.definition);
const mutable = ref<CustomFormData>(props.modelValue.find((response) => response.form === props.form.id)?.data || {});

const existingResponse = computed<CustomFormResponse | undefined>(() => {
  return responses.value.find((response) => response.form === props.form.id);
});

props.form.definition.fieldsets.forEach((fieldset) => {
  fieldset.fields.forEach((field) => {
    if (!mutable.value[field.code]) {
      if ((field.type === 'select' || field.type === 'option_group') && field.multiple) {
        mutable.value[field.code] = [];
        if (field.other_option) {
          mutable.value[`${field.code}__other`] = '';
        }
      } else {
        mutable.value[field.code] = '';
      }
    }
  });
});

const formIsValid = computed<boolean>(() => {
  return props.form.definition.fieldsets.every((fieldset) => {
    return fieldset.fields.every((field) => {
      if (field.required) {
        if ((field.type === 'select' || field.type === 'option_group') && field.multiple) {
          return (mutable.value[field.code] as []).length > 0;
        } else {
          return mutable.value[field.code] !== '';
        }
      }
      return true;
    });
  });
});

function isInputField(field: ChoiceField | InputField): field is InputField {
  return ['text', 'number', 'date', 'email', 'tel', 'url'].includes(field.type);
}

function getTextValue(translation: Translation): string {
  return translation[locale.value as 'en' | 'nl'] || translation.nl;
}

const translatedFormDefinition = computed<CustomFormDefinition>(() => {
  const formDefinition = cloneDeep(definition.value);

  formDefinition.fieldsets.forEach((fieldset) => {
    fieldset.fields.forEach((field) => {
      if ((field.type === 'select' || field.type === 'option_group') && field.options) {
        field.options = (field.options as FieldOption[]).map((option) => {
          return {
            ...option,
            label: locale.value === 'en' ? option.label.en : option.label.nl,
          };
        }) as TranslatedFieldOption[];
      }
    });
  });

  return formDefinition;
});

function save(): void {
  if (existingResponse.value) {
    api.put(existingResponse.value.self, { data: mutable.value, form: existingResponse.value.form }).then((res) => {
      const idx = responses.value.findIndex((r) => r.id === res.data.id);
      responses.value[idx] = res.data;
      emit('update:modelValue', responses.value);
    });
  } else {
    api.post(props.apiEndpoint, { data: mutable.value, form: props.form.id }).then((res) => {
      responses.value.push(res.data);
      emit('update:modelValue', responses.value);
    });
  }
}
</script>
