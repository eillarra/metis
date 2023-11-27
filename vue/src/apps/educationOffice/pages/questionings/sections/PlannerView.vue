<template>
  <div class="row q-col-gutter-xl">
    <div class="col-12 col-md">
      <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive header-nav>
        <q-step :name="1" title="Zijn er studenten die hun eerste keuze zullen krijgen?" icon="person_search" active-icon="person_add">
          <p>Deze studenten worden sowieso toegewezen aan de plaats die ze als eerste keuze hebben gekozen.</p>
          <api-autocomplete
            v-model="formData.students_first_choice"
            clearable
            :data-source="students"
            :mapper="studentMapper"
            :label="$t('student', 9)"
            :multiple="true"
          />
          <q-stepper-navigation class="flex">
            <q-btn
              unelevated
              @click="step = 2"
              color="blue-1"
              text-color="ugent"
              :label="$t('form.skip')"
            />
            <q-space />
          </q-stepper-navigation>
        </q-step>
        <q-step :name="2" title="Zijn er stageplaatsen die altijd in de planning moeten worden opgenomen?" icon="business" active-icon="domain_add">
          <p>De student die deze plaats het hoogst in zijn / haar tops heeft gekozen, wordt aan deze plaats toegewezen. U kunt meerdere plaatsen kiezen en de planner zal zijn best doen om de studenten aan deze plaatsen toe te wijzen.</p>
          <api-autocomplete
            v-model="formData.places_with_students"
            clearable
            :data-source="projectPlaces"
            :mapper="placeMapper"
            :label="$t('place')"
            :multiple="true"
          />
        </q-step>
      </q-stepper>
    </div>
    <div class="col-12 col-md-4">
      <q-card flat class="bg-grey-2 q-pa-md text-right q-mt-md">
        <span class="text-h5 text-ugent">
          <a :href="`/nl/files/q/planning/${questioning.id}.pdf?${queryParamsString}`" target="_blank"><q-icon name="download" /></a>
        </span>
        <small class="float-left">Planningsvoorstel (PDF)</small>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

import ApiAutocomplete from '@/components/forms/ApiAutocomplete.vue';

defineProps<{
  questioning: Questioning;
  students: Student[];
  projectPlaces: ProjectPlace[];
}>();

const step = ref(1);
const formData = ref({
  students_first_choice: [] as number[],
  places_with_students: [] as number[],
});

const queryParamsString = computed<string>(() => {
  const params = new URLSearchParams();
  const queryParams = {
    students_first_choice: formData.value.students_first_choice.map((obj) => obj.id),
    places_with_students: formData.value.places_with_students.map((obj) => obj.id),
  };

  Object.keys(queryParams).forEach((key) => {
    const value = queryParams[key];
    if (value.length > 0) {
      params.append(key, value.join(','));
    }
  });

  return params.toString();
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
