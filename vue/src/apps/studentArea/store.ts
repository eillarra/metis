import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios.ts';

export const useStore = defineStore('studentArea', () => {
  const education = ref<EducationTiny | undefined>(undefined);
  const internships = ref<Internship[]>([]);
  const signatures = ref<Signature[] | undefined>(undefined);
  const students = ref<Student[]>([]);
  const projects = ref<Project[]>([]);
  const projectPlaceOptions = ref<ProjectPlaceOption[]>([]);

  const selectedProjectId = ref<number | null>(null);

  async function init() {
    await fetchSignatures();
  }

  async function fetchSignatures() {
    signatures.value = undefined;

    await api.get('/user/student/signatures/').then((res) => {
      signatures.value = res.data;
    });
  }

  function setData(
    djangoEducation: EducationTiny,
    djangoProjects: Project[],
    djangoStudents: Student[],
    djangProjectPlaceOptions: ProjectPlaceOption[],
    djangoInternships: Internship[]
  ) {
    djangoProjects.sort((a, b) => {
      return new Date(b.start_date).getTime() - new Date(a.start_date).getTime();
    });
    education.value = djangoEducation;
    students.value = djangoStudents;
    // TODO: move to an external fuction as it is very similar to placeOffice/store.ts
    projects.value = djangoProjects.map((project) => {
      const periods = project.periods;
      const questionings = project.questionings.map((date) => {
        date.Period = periods.find((period) => period.id === date.period) || undefined;
        return date;
      });
      return {
        ...project,
        questionings,
      };
    });
    selectedProjectId.value = djangoProjects[0]?.id || null;
    projectPlaceOptions.value = djangProjectPlaceOptions;
    internships.value = djangoInternships.map((internship) => ({
      ...internship,
    }));
  }

  const project = computed<Project | undefined>(() => {
    return projects.value.find((p: Project) => p.id === selectedProjectId.value);
  });

  const activeQuestionings = computed<Questioning[]>(() => {
    const validTypes: string[] = ['student_information', 'student_tops'];
    return project.value?.questionings.filter((date) => date.is_active && validTypes.includes(date.type)) ?? [];
  });

  function updateCollection(type: string, action: string, obj: ApiObject) {
    let collection: ApiObject[] = [];

    switch (type) {
      case 'internship':
        collection = internships.value as Internship[];
        break;
      default:
        break;
    }

    const idx: number = collection.findIndex((row: ApiObject) => row.id === obj.id);

    switch (action) {
      case 'update':
        Object.assign(collection[idx], cloneDeep(obj));
        break;
      default:
        break;
    }
  }

  function updateObj(type: string, obj: ApiObject) {
    updateCollection(type, 'update', obj);
  }

  return {
    init,
    setData,
    fetchSignatures,
    updateObj,
    education,
    internships,
    project,
    projectPlaceOptions,
    activeQuestionings,
    signatures,
    students,
  };
});
