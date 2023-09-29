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
              <q-item section side v-if="scope.opt.disable || scope.opt.disciplineDisable">
                <q-badge v-if="skipPlaceIds.includes(scope.opt.place_id)" color="ugent">Geweest</q-badge>
                <q-badge v-else-if="scope.opt.disciplineDisable" color="red">{{ scope.opt.disciplines }}</q-badge>
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
  questioning: Questioning;
  modelValue: CustomFormResponse[];
  projectPlaceOptions: ProjectPlaceOption[];
  skipPlaceIds: number[];
  skipDisciplineIds: number[];
}>();

const choices = [...Array((props.questioning.form_definition as TopsFormDefinition).num_tops).keys()];
const pdf =
  props.questioning.form_definition.num_tops == 10
    ? '/nl/stages/logo/files/p/20/project_place_information.pdf'
    : '/nl/stages/audio/files/p/11/project_place_information.pdf';
const responses = ref<CustomFormResponse[]>(props.modelValue);
const definition = ref<TopsFormDefinition>(props.questioning.form_definition as TopsFormDefinition);
const mutable = ref<CustomFormData>(
  props.modelValue
    .find((response) => response.questioning === props.questioning.id)
    ?.data.tops.map((id: number) => ({
      value: id,
      label: props.projectPlaceOptions.find((option) => option.value === id)?.label,
    })) || []
);
const skipPlaceIds = computed<number[]>(() => props.skipPlaceIds);

const formTitle = computed<string>(() => {
  if (definition.value.title) {
    return locale.value === 'en' ? definition.value.title.en : definition.value.title.nl;
  }
  return 'Form';
});

const existingResponse = computed<CustomFormResponse | undefined>(() => {
  return responses.value.find((response) => response.questioning === props.questioning.id);
});

const formIsValid = computed<boolean>(() => {
  const tops = mutable.value.filter((option: ProjectPlaceOption | null) => option);
  return tops.length === definition.value.num_tops;
});

function save(): void {
  // remove null values from mutable
  const tops = {
    tops: mutable.value
      .filter((option: ProjectPlaceOption | null) => option)
      .map((option: ProjectPlaceOption) => option.value),
  };

  if (existingResponse.value) {
    api
      .put(existingResponse.value.self, { data: tops, questioning: existingResponse.value.questioning })
      .then((res) => {
        const idx = responses.value.findIndex((r) => r.id === res.data.id);
        responses.value[idx] = res.data;
        notify.success(t('form.updated'));
        emit('update:modelValue', responses.value);
      });
  } else {
    api.post(props.apiEndpoint, { data: tops, questioning: props.questioning.id }).then((res) => {
      responses.value.push(res.data);
      notify.success(t('form.saved'));
      emit('update:modelValue', responses.value);
    });
  }
}

const tops = computed(() =>
  mutable.value.filter((option: ProjectPlaceOption | null) => option).map((option: ProjectPlaceOption) => option.value)
);

const options = computed(() => {
  return props.projectPlaceOptions.map((option) => {
    const d = props.skipDisciplineIds;
    const disciplineDisable =
      (d.length == 2 && d[0] == 1 && d[1] == 1 && option.disciplines == 'Klinisch') ||
      (d.length == 2 && d[0] == 2 && d[1] == 2 && option.disciplines == 'Prothetisch');

    return {
      ...option,
      disable: tops.value.includes(option.value) || props.skipPlaceIds.includes(option.place_id) || disciplineDisable,
      disciplineDisable: disciplineDisable,
    };
  });
});
</script>
