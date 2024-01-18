import { ref } from 'vue';
import { defineStore } from 'pinia';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios.ts';

export const useStore = defineStore('placeOffice', () => {
  const education = ref<EducationTiny>();
  const internships = ref<Internship[]>([]);

  async function init() {
    await fetchInternships();
  }

  function setData(djangoEducation: EducationTiny) {
    education.value = djangoEducation;
  }

  function updateInternship(obj: Internship) {
    const idx: number = internships.value.findIndex((row: Internship) => row.id === obj.id);
    Object.assign(internships.value[idx], cloneDeep(obj));
  }

  function fetchInternships() {
    api.get('/user/student/preplanned-internships/').then((res) => {
      internships.value = res.data;
    });
  }

  return {
    init,
    setData,
    updateInternship,
    education,
    internships,
  };
});
