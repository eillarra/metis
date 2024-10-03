<template>
  <!-- TODO: extend this with extra fields -->
  <div>
    <div v-for="(fieldset, idx) in formDefinition.fieldsets" :key="`fieldset-${idx}`">
      <div v-for="field in fieldset.fields" :key="field.code">
        <div v-if="field.type == 'composite' && ((data[field.code] as []) || []).length">
          <h5 class="text-body1">{{ field.label[lang] }}</h5>
          <q-markup-table flat dense class="ugent__data-table dense">
            <thead class="text-left">
              <tr>
                <th v-for="subfield in field.fields" :key="subfield.code">
                  {{ subfield.label[lang] }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(obj, i) in data[field.code]" :key="`entry-${i}`">
                <td v-for="subfield in field.fields" :key="subfield.code">
                  <span v-if="subfield.type == 'select'">{{
                    getOptionDisplay(obj[subfield.code], subfield.options)
                  }}</span>
                  <span v-else>{{ obj[subfield.code] ?? '' }}</span>
                </td>
              </tr>
            </tbody>
          </q-markup-table>
        </div>
        <div v-else-if="data[field.code]">
          <h5 class="text-body1 q-mt-lg q-mb-sm">{{ field.label[lang] }}</h5>
          <p>{{ data[field.code] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue';
import { useI18n } from 'vue-i18n';

defineProps<{
  formDefinition: CustomFormDefinition;
  data: CustomFormData;
}>();

const { locale } = useI18n();

const lang = computed<'en' | 'nl'>(() => (locale.value === 'en' ? 'en' : 'nl'));

interface FieldOption {
  value: string | number | null;
  label: Translation;
}

function getOptionDisplay(option: string, options: FieldOption[]) {
  const optionsDict = options.reduce(
    (acc, cur) => {
      acc[cur.value as string] = cur.label[locale.value as 'en' | 'nl'];
      return acc;
    },
    {} as Record<string | number, string>,
  );

  return optionsDict[option] || option;
}
</script>
