import { computed, ref, watch } from 'vue';
import { defineStore } from 'pinia';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios.ts';
import { find } from 'lodash-es';

export const useStore = defineStore('educationOffice', () => {
  const education = ref<Education | null>(null);
  const programs = ref<Program[]>([]);
  const projects = ref<Project[]>([]);
  const projectInternships = ref<Internship[]>([]);
  const projectPlaces = ref<ProjectPlace[]>([]);
  const students = ref<Student[]>([]);

  const selectedProjectId = ref<number | null>(null);

  const programInternshipMap = computed<Map<number, ProgramInternship>>(() => {
    if (!programs.value) {
      return new Map();
    }

    const internships = new Map<number, ProgramInternship>();

    programs.value.forEach((program) => {
      program.blocks.forEach((block) => {
        if (!block.internships || !block.internships.length) {
          return;
        }
        block.internships.forEach((internship) => {
          if (!internships.has(internship.id)) {
            internships.set(internship.id, {
              ...internship,
              block: block,
            });
          }
        });
      });
    });

    return internships;
  });

  const project = computed<Project | undefined>(() => {
    const selectedProject = projects.value.find((p: Project) => p.id === selectedProjectId.value);

    if (!selectedProject) {
      return undefined;
    }

    selectedProject.periods = selectedProject.periods.map((period) => {
      period.program_internship =
        programInternshipMap.value.get(period.program_internship as number) || period.program_internship;
      return period;
    });

    return selectedProject;
  });

  const projectStudents = computed<ProjectStudent[]>(() => {
    if (!project.value || !students.value.length) {
      return [];
    }

    return students.value.reduce((arr, student) => {
      student.student_set.forEach((obj) => {
        if (obj.project.id === project.value?.id) {
          arr.push(obj);
        }
      });
      return arr;
    }, [] as ProjectStudent[]);
  });

  const contacts = computed<Contact[]>(() => {
    const ids: Set<number> = new Set();
    const output: Contact[] = [];

    places.value.forEach((obj: Place) => {
      if (!obj.contacts || !obj.contacts.length) {
        return;
      }

      obj.contacts.forEach((contact: Contact) => {
        if (!ids.has(contact.id)) {
          ids.add(contact.id);
          output.push({
            ...contact,
            place: {
              ...obj,
              contacts: [], // just make the object smaller
            },
          });
        }
      });
    });

    return output;
  });

  const places = computed<Place[]>(() => {
    return projectPlaces.value.map((obj) => obj.place);
  });

  const projectPlacesWithInternships = computed<Set<number>>(() => {
    return projectInternships.value.reduce((set, obj) => {
      set.add(obj.project_place);
      return set;
    }, new Set<number>());
  });

  const projectStudentsWithInternships = computed<Set<number>>(() => {
    return projectInternships.value.reduce((set, obj) => {
      set.add(obj.student);
      return set;
    }, new Set<number>());
  });

  const projectPlaceMap = computed<Map<number, Place>>(() =>
    projectPlaces.value.reduce((map, obj) => {
      map.set(obj.id, obj.place);
      return map;
    }, new Map())
  );

  const internships = computed<Internship[]>(() => {
    if (!project.value || !projectPlaces.value.length || !students.value.length) {
      return [];
    }

    const periodMap: Map<number, Period> = project.value.periods.reduce((map, period) => {
      map.set(period.id, period);
      return map;
    }, new Map());

    const studentMap: Map<number, Student> = students.value.reduce((map, student) => {
      const studentObjectId = find(student.student_set, { project: { id: project.value?.id } })?.id;
      map.set(studentObjectId, student);
      return map;
    }, new Map());

    return projectInternships.value.map((obj: Internship) => {
      return {
        ...obj,
        period: periodMap.get(obj.period) || obj.period,
        place: projectPlaceMap.value.get(obj.project_place),
        student: studentMap.get(obj.student) || obj.student,
      };
    });
  });

  async function init() {
    await fetchStudents();
    await fetchProjectPlaces();
    await fetchInternships();
  }

  async function fetchInternships() {
    projectInternships.value = [];

    if (!project.value) {
      return;
    }

    await api.get(project.value.rel_internships).then((res) => {
      projectInternships.value = res.data;
    });
  }

  async function fetchProjectPlaces() {
    projectPlaces.value = [];

    if (!project.value) {
      return;
    }

    await api.get(project.value.rel_places).then((res) => {
      projectPlaces.value = res.data;
    });
  }

  async function fetchStudents() {
    students.value = [];

    if (!project.value) {
      return;
    }

    await api.get(project.value.rel_students).then((res) => {
      students.value = res.data;
    });
  }

  function setData(djangoEducation: Education, djangoPrograms: Program[], djangoProjects: Project[]) {
    education.value = djangoEducation;
    programs.value = djangoPrograms;
    projects.value = djangoProjects;
    selectedProjectId.value = djangoProjects[0]?.id || null;
  }

  function updateCollection(type: string, action: string, obj: ApiObject) {
    let collection: ApiObject[] = [];

    switch (type) {
      case 'contact':
        const placeId =
          typeof (obj as Contact).place === 'number' ? (obj as Contact).place : ((obj as Contact).place as Place).id;
        collection = places.value.find((row) => row.id === placeId)?.contacts as Contact[];
        break;
      case 'projectInternship':
        collection = projectInternships.value as Internship[];
        break;
      case 'projectPlace':
        collection = projectPlaces.value as ProjectPlace[];
        break;
      case 'student':
        if (action == 'insert') {
          fetchStudents();
          return;
        }
        collection = students.value as Student[];
        break;
      default:
        break;
    }

    const idx: number = collection.findIndex((row: ApiObject) => row.id === obj.id);

    switch (action) {
      case 'insert':
        collection.push(cloneDeep(obj));
        break;
      case 'update':
        Object.assign(collection[idx], cloneDeep(obj));
        break;
      case 'remove':
        collection.splice(idx, 1);
        break;
      default:
        break;
    }
  }

  function createObj(type: string, obj: ApiObject) {
    updateCollection(type, 'insert', obj);
  }

  function updateObj(type: string, obj: ApiObject) {
    updateCollection(type, 'update', obj);
  }

  function deleteObj(type: string, obj: ApiObject) {
    updateCollection(type, 'remove', obj);
  }

  watch(selectedProjectId, (id) => {
    if (id) {
      init();
    }
  });

  return {
    init,
    setData,
    createObj,
    updateObj,
    deleteObj,
    education,
    contacts,
    internships,
    places,
    programs,
    projects,
    project,
    projectPlaces,
    projectPlacesWithInternships,
    projectStudents,
    projectStudentsWithInternships,
    selectedProjectId,
    students,
  };
});
