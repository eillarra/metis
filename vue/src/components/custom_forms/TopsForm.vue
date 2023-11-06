<template>
  <dialog-form icon="fact_check" :title="formTitle">
    <template #page>
      <div v-if="triageQuestion">
        <p class="q-pa-lg">{{ triageQuestion }}</p>
        <q-option-group
          v-model="mutableTriage"
          :options="[{ label: 'Ja', value: true }, { label: 'Nee', value: false }]"
          color="ugent"
          dense
          inline
          class="q-mb-lg"
        />
        <q-separator />
      </div>
      <div v-show="!mutableTriage">
        <p class="q-pa-lg" v-if="formDescription">{{ formDescription }}</p>
        <div class="q-px-lg q-mb-lg q-gutter-y-md">
          <div v-for="num in choices" :key="num">
            <q-select
              filled
              dense
              clearable
              v-model="mutableTops[num]"
              use-input
              input-debounce="0"
              :label="`#${num + 1}`"
              :options="options"
              class="q-mb-sm"
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
            <q-input v-if="requireMotivation" dense label="Motivatie" v-model="mutableMotivation[num]" />
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="row q-ma-lg">
        <div class="col-12 col-md text-dark">
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
import { computed, ref, onMounted, watch } from 'vue';
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
  skipPlaceIds: number[] | null;
  skipDisciplineIds: number[] | null;
}>();

const choices = [...Array((props.questioning.form_definition as TopsFormDefinition).num_tops).keys()];
const responses = ref<CustomFormResponse[]>(props.modelValue);
const response = computed<TopsFormResponse | undefined>(() => {
  return responses.value.find((response) => response.questioning === props.questioning.id) as
    | TopsFormResponse
    | undefined;
});
const definition = ref<TopsFormDefinition>(props.questioning.form_definition as TopsFormDefinition);
const skipPlaceIds = computed<number[]>(() => props.skipPlaceIds || []);
const requireMotivation = computed<boolean>(() => definition.value.require_motivation || false);
const triageQuestion = computed<string | null>(() =>
  definition.value.triage_question ? definition.value.triage_question[locale.value] : null
);

const mutableTriage = ref<boolean | null>(null);
const mutableTops = ref<ProjectPlaceOption[]>([]);
const mutableMotivation = ref<string[]>([]);

const tops = computed(() =>
  mutableTops.value
    .filter((option: ProjectPlaceOption | null) => option)
    .map((option: ProjectPlaceOption) => option.value)
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

const formIsValid = computed<boolean>(() => {
  if (mutableTriage.value === true) {
    return true;
  }

  const tops = mutableTops.value.filter((option: ProjectPlaceOption | null) => option);

  if (requireMotivation.value) {
    return tops.length === definition.value.num_tops && mutableMotivation.value.length === definition.value.num_tops;
  } else {
    return tops.length === definition.value.num_tops;
  }
});

function save(): void {
  let massagedData = {};

  if (mutableTriage.value === true) {
    massagedData = {
      tops: null,
    };
  } else {
    // remove null values from mutable
    massagedData = {
      tops: mutableTops.value
        .filter((option: ProjectPlaceOption | null) => option)
        .map((option: ProjectPlaceOption) => option.value),
    };

    if (requireMotivation.value) {
      // convert list of remarks to an object, based on tops order
      // so we combine the tops and motivation lists into one object
      massagedData['motivation'] = mutableMotivation.value.reduce((obj: any, item: string, index: number) => {
        obj[mutableTops.value[index].value] = item;
        return obj;
      }, {});
    }
  }

  if (existingResponse.value) {
    api
      .put(existingResponse.value.self, { data: massagedData, questioning: existingResponse.value.questioning })
      .then((res) => {
        const idx = responses.value.findIndex((r) => r.id === res.data.id);
        responses.value[idx] = res.data;
        notify.success(t('form.updated'));
        emit('update:modelValue', responses.value);
      });
  } else {
    api.post(props.apiEndpoint, { data: massagedData, questioning: props.questioning.id }).then((res) => {
      responses.value.push(res.data);
      notify.success(t('form.saved'));
      emit('update:modelValue', responses.value);
    });
  }
}

const options = computed(() => {
  return props.projectPlaceOptions.map((option) => {
    const d = props.skipDisciplineIds || [];
    const disciplineDisable =
      (d.length == 2 && d[0] == 1 && d[1] == 1 && option.disciplines == 'Klinisch') ||
      (d.length == 2 && d[0] == 2 && d[1] == 2 && option.disciplines == 'Prothetisch');

    return {
      ...option,
      disable: tops.value.includes(option.value) || skipPlaceIds.value.includes(option.place_id) || disciplineDisable,
      disciplineDisable: disciplineDisable,
    };
  });
});

function updateMutables(res: TopsFormResponse): void {
  if (res) {
    if (definition.value.triage_question) {
      mutableTriage.value = res?.data.tops == null ? true : false;
    }

    if (res?.data.tops === null) {
      mutableTops.value = [];
      mutableMotivation.value = [];
      return;
    }

    mutableTops.value = res.data.tops?.map((top: number) => {
      return props.projectPlaceOptions.find((option) => option.value === top) as ProjectPlaceOption;
    });
    const m: string[] = [];
    res?.data.tops?.forEach((id: number) => {
      if (res?.data.motivation && res?.data.motivation[id]) {
        m.push(res?.data.motivation[id]);
      } else {
        m.push('');
      }
    });
    mutableMotivation.value = m;
  } else {
    mutableTops.value = [];
    mutableMotivation.value = [];
  }
}

watch(response, (val) => {
  updateMutables(val);
});

onMounted(() => {
  if (response.value) updateMutables(response.value);
});
</script>
