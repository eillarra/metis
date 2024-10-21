<template>
  <div class="row q-col-gutter-xl">
    <div class="col-12 col-md">
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" title="Zijn er studenten die hun eerste keuze zullen krijgen?" :icon="iconStudent">
          <p>Deze studenten worden sowieso toegewezen aan de plaats die ze als eerste keuze hebben gekozen.</p>
          <api-autocomplete
            v-model="formData.students_with_first_choice"
            clearable
            :data-source="students"
            :mapper="studentMapper"
            :label="$t('student', 9)"
            :multiple="true"
          />
          <q-stepper-navigation class="flex">
            <q-btn unelevated @click="step = 2" color="blue-1" text-color="ugent" :label="$t('form.skip')" />
            <q-space />
          </q-stepper-navigation>
        </q-step>
        <q-step
          :name="2"
          title="Zijn er stageplaatsen die altijd in de planning moeten worden opgenomen?"
          :icon="iconPlace"
        >
          <p>
            De student die deze plaats het hoogst in zijn / haar tops heeft gekozen, wordt aan deze plaats toegewezen. U
            kunt meerdere plaatsen kiezen en de planner zal zijn best doen om de studenten aan deze plaatsen toe te
            wijzen.
          </p>
          <api-autocomplete
            v-model="formData.places_with_students"
            clearable
            :data-source="projectPlaces"
            :mapper="placeMapper"
            :label="$t('place', 9)"
            :multiple="true"
          />
          <q-stepper-navigation class="flex">
            <q-btn unelevated @click="step = 3" color="blue-1" text-color="ugent" :label="$t('form.skip')" />
            <q-space />
          </q-stepper-navigation>
        </q-step>
        <q-step
          :name="3"
          title="Zijn er studenten of stageplaatsen dat u wil weglaten uit de planning?"
          :icon="iconTableBoolFalse"
        >
          <p>
            Deze studenten en stageplaatsen zullen niet worden opgenomen in de planning. U kunt meerdere studenten en
            stageplaatsen kiezen.
          </p>
          <api-autocomplete
            v-model="formData.students_to_skip"
            clearable
            :data-source="students"
            :mapper="studentMapper"
            :label="$t('student', 9)"
            :multiple="true"
          />
          <api-autocomplete
            v-model="formData.places_to_skip"
            clearable
            :data-source="projectPlaces"
            :mapper="placeMapper"
            :label="$t('place', 9)"
            :multiple="true"
          />
        </q-step>
      </q-stepper>
    </div>
    <div class="col-12 col-md-4">
      <q-card flat class="bg-grey-2 q-pa-md text-right q-mt-md">
        <span class="text-h5 text-ugent">
          <a :href="`/nl/files/q/planning/${questioning.id}.xlsx${queryParamsString}`" target="_blank">
            <q-icon :name="iconDownload" />
          </a>
        </span>
        <small class="float-left">Planningsvoorstel (Excel)</small>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

import ApiAutocomplete from '@/components/forms/ApiAutocomplete.vue';

import { iconDownload, iconPlace, iconStudent, iconTableBoolFalse } from '@/icons';

defineProps<{
  questioning: Questioning;
  students: Student[];
  projectPlaces: ProjectPlace[];
}>();

const step = ref(1);
const formData = ref({
  students_with_first_choice: [] as Student[],
  students_to_skip: [] as Student[],
  places_with_students: [] as ProjectPlace[],
  places_to_skip: [] as ProjectPlace[],
});

const queryParamsString = computed<string>(() => {
  const params = new URLSearchParams();
  const queryParams = {
    s_first: formData.value.students_with_first_choice.map((obj) => obj.id),
    s_skip: formData.value.students_to_skip.map((obj) => obj.id),
    p_force: formData.value.places_with_students.map((obj) => obj.id),
    p_skip: formData.value.places_to_skip.map((obj) => obj.id),
  };

  Object.keys(queryParams).forEach((key) => {
    const value = queryParams[key];
    if (value.length > 0) {
      params.append(key, value.join(','));
    }
  });

  return params.toString() ? `?${params.toString()}` : '';
});

function studentMapper(data: ApiObject[]) {
  return data.map((obj) => ({
    id: obj.id,
    name: (obj as Student).User?.name,
    caption: (obj as Student).User?.email,
  }));
}

function placeMapper(data: ApiObject[]) {
  return data.map((obj) => {
    return {
      id: obj.id,
      name: (obj as ProjectPlace).place.name,
      caption: `${(obj as ProjectPlace).place.Type?.name}`,
    };
  });
}
</script>
