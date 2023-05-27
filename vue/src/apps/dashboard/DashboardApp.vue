<template>
  <div class="row ugent__submenu q-mb-lg">
    <div class="menu-item">
      <span>Dashboard</span>
    </div>
  </div>
  <div class="row q-col-gutter-lg">
    <div v-if="educations.length" class="col-12 col-md-3">
      <ugent-link-list :title="$t('dashboard.education_office')" :items="educationLinks" />
    </div>
    <div v-if="places.length" class="col-12 col-md-3">
      <ugent-link-list :title="$t('dashboard.place_office')" :items="placesLinks" />
    </div>
    <div v-if="student_educations.length" class="col-12 col-md-3">
      <ugent-link-list :title="$t('dashboard.my_internships')" :items="studentLinks" />
    </div>
    <div v-if="!educations.length && !student_educations.length && !places.length" class="col-12 col-md-3">
      <h4 class="q-mt-none q-mb-md">{{ $t('dashboard.my_internships') }}</h4>
      <p>{{ $t('dashboard.no_results') }}.</p>
    </div>
  </div>
  <ugent-banner>
    <template #default>
      <div class="fit column justify-between">
        <q-space />
        <!--<ugent-link-list title="Help" :items="links" />-->
      </div>
    </template>
    <template #image>
      <img src="@/assets/uzgent.jpg" />
    </template>
  </ugent-banner>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { usePage } from '@inertiajs/vue3';

import UgentBanner from '@/components/UgentBanner.vue';
import UgentLinkList from '@/components/UgentLinkList.vue';

const page = usePage();

const educations = computed<Education[]>(() => page.props.educations as Education[]);
const places = computed<Place[]>(() => page.props.places as Place[]);
const student_educations = computed<EducationTiny[]>(() => page.props.student_educations as EducationTiny[]);

const educationLinks = computed(() =>
  educations?.value.map((education) => ({
    label: education.short_name,
    href: education.url,
  }))
);

const placesLinks = computed(() =>
  places.value.map((place) => ({
    label: place.name,
    href: '../places/' + place.id + '/',
  }))
);

const studentLinks = computed(() =>
  student_educations.value.map((educationTiny) => ({
    label: educationTiny.short_name,
    href: '../stages/' + educationTiny.code + '/',
  }))
);
</script>
