<template>
  <dialog-form icon="fact_check" :title="formTitle">
    <template #page>
      <p class="q-pa-lg">
        Een aantal stageplaatsen bezorgde ons reeds een ingevulde informatiefiche. Hierin kunnen jullie gegevens
        betreffende de patiëntenpopulatie, vereiste voorkennis, uurrooster,... terugvinden [<a
          :href="pdf"
          target="_blank"
          >PDF</a
        >]
      </p>
      <div class="q-px-lg q-mb-lg q-gutter-y-md">
        <q-select
          v-for="num in choices"
          :key="num"
          filled
          dense
          clearable
          v-model="mutable[num]"
          use-input
          input-debounce="0"
          :label="`#${num + 1}`"
          :options="options"
        >
          <template #option="scope">
            <q-item v-bind="scope.itemProps">
              <q-item-section>
                <q-item-label>{{ scope.opt.label }}</q-item-label>
                <q-item-label caption>{{ scope.opt.disciplines }}</q-item-label>
              </q-item-section>
              <q-item section side v-if="scope.opt.disable">
                <q-badge v-if="scope.opt.place_id == props.skipPlaceId" color="ugent">Ba3</q-badge>
                <q-icon v-else name="check_circle" />
              </q-item>
            </q-item>
          </template>
        </q-select>
      </div>
    </template>
    <template #footer>
      <div class="row q-ma-lg">
        <div class="col-12 col-md">
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
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { api } from '@/axios';
import { notify } from '@/notify';

import DialogForm from '../forms/DialogForm.vue';

const { t, locale } = useI18n();

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  form: TopsForm;
  modelValue: CustomFormResponse[];
  projectPlaceOptions: ProjectPlaceOption[];
  skipPlaceId: number | null;
}>();

const choices = [...Array(props.form.definition.num_tops).keys()];
const pdf =
  props.form.definition.num_tops == 10
    ? '/nl/stages/logo/files/p/20/project_place_information.pdf'
    : '/nl/stages/audio/files/p/10/project_place_information.pdf';
const responses = ref<CustomFormResponse[]>(props.modelValue);
const definition = ref<TopsFormDefinition>(props.form.definition);
const mutable = ref<CustomFormData>(
  props.modelValue
    .find((response) => response.form === props.form.id)
    ?.data.tops.map((id: number) => ({
      value: id,
      label: props.projectPlaceOptions.find((option) => option.value === id)?.label,
    })) || []
);

const formTitle = computed<string>(() => {
  if (definition.value.title) {
    return locale.value === 'en' ? definition.value.title.en : definition.value.title.nl;
  }
  return 'Form';
});

const existingResponse = computed<CustomFormResponse | undefined>(() => {
  return responses.value.find((response) => response.form === props.form.id);
});

const formIsValid = computed<boolean>(() => {
  const tops = mutable.value.filter((option: ProjectPlaceOption | null) => option);
  return tops.length === props.form.definition.num_tops;
});

function save(): void {
  // remove null values from mutable
  const tops = {
    tops: mutable.value
      .filter((option: ProjectPlaceOption | null) => option)
      .map((option: ProjectPlaceOption) => option.value),
  };

  if (existingResponse.value) {
    api.put(existingResponse.value.self, { data: tops, form: existingResponse.value.form }).then((res) => {
      const idx = responses.value.findIndex((r) => r.id === res.data.id);
      responses.value[idx] = res.data;
      notify.success(t('form.updated'));
      emit('update:modelValue', responses.value);
    });
  } else {
    api.post(props.apiEndpoint, { data: tops, form: props.form.id }).then((res) => {
      responses.value.push(res.data);
      notify.success(t('form.saved'));
      emit('update:modelValue', responses.value);
    });
  }
}

const tops = computed(() =>
  mutable.value.filter((option: ProjectPlaceOption | null) => option).map((option: ProjectPlaceOption) => option.value)
);

const options = computed(() =>
  props.projectPlaceOptions.map((option) => {
    return {
      ...option,
      disable: tops.value.includes(option.value) || option.place_id == props.skipPlaceId,
    };
  })
);
</script>
