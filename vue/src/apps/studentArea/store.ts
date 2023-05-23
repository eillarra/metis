import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useStore = defineStore('studentArea', () => {
  const education = ref<EducationTiny | null>(null);
  const projectStudents = ref<ProjectStudent[]>([]);

  async function init() {}

  function setData(djangoEducation: EducationTiny, djangoProjectStudents: ProjectStudent[]) {
    education.value = djangoEducation;
    projectStudents.value = djangoProjectStudents;
  }

  return {
    init,
    setData,
    projectStudents,
  };
});
