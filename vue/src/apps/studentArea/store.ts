import { ref } from 'vue';
import { defineStore } from 'pinia';

import { api } from '@/axios.ts';

export const useStore = defineStore('studentArea', () => {
  const education = ref<EducationTiny | undefined>(undefined);
  const signatures = ref<Signature[] | undefined>(undefined);
  const students = ref<Student[]>([]);

  async function init() {
    await fetchSignatures();
  }

  async function fetchSignatures() {
    signatures.value = undefined;

    await api.get('/user/student/signatures/').then((res) => {
      signatures.value = res.data;
    });
  }

  function setData(djangoEducation: EducationTiny, djangoStudents: Student[]) {
    education.value = djangoEducation;
    students.value = djangoStudents;
  }

  return {
    init,
    setData,
    fetchSignatures,
    education,
    signatures,
    students,
  };
});
