<template>
  <dialog-form icon="tag" :title="$t('availability')">
    <template #page>
      <div class="q-px-lg">
        <div v-for="period in visiblePeriods" :key="period.id" class="row q-col-gutter-md">
          <q-field dense readonly :label="$t('period')" class="col-6 col-md-6" stack-label>
            <template #control>
              <span>{{ period.start_date }} - {{ period.end_date }}</span>
            </template>
          </q-field>
          <q-input dense type="number" v-model="data[period.id].min" label="Min" class="col-6 col-md-3" />
          <q-input dense type="number" v-model="data[period.id].max" label="Max" class="col-6 col-md-3" />
        </div>
      </div>
    </template>
    <template #footer>
      <q-btn @click="save" unelevated color="ugent" :label="$t('form.update')" class="float-right q-ma-lg" />
    </template>
  </dialog-form>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

import DialogForm from '@/components/forms/DialogForm.vue';

const props = defineProps<{
  project: Project;
}>();

const data = ref({});
const visiblePeriods = computed<Period[]>(() => {
  const tmpSet = new Set([1, 2, 3, 4]);
  return props.project.periods.filter((period) => tmpSet.has(period.program_internship));
});

// add default values to data
visiblePeriods.value.forEach((period) => {
  data.value[period.id] = {
    min: 0,
    max: 0,
  };
});

function save() {
  console.log('save');
}
</script>
