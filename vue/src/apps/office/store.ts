import { computed, ref, watch } from 'vue';
import { defineStore } from 'pinia';

import { api } from '@/axios.ts';
import { find } from 'lodash-es';

export const useOfficeStore = defineStore('office', () => {
  const education = ref<Education | null>(null);
  const educationPlaces = ref<EducationPlace[]>([]);
  const programs = ref<Program[]>([]);
  const projects = ref<Project[]>([]);
  const projectInternships = ref<Internship[]>([]);
  const projectPlaces = ref<ProjectPlace[]>([]);
  const projectStudents = ref<Student[]>([]);

  const selectedProjectId = ref<number | null>(null);

  const project = computed<Project | null>(() => {
    return projects.value?.find((p) => p.id === selectedProjectId.value) || null;
  });

  const placeMapForProject = computed<Map<number, Place>>(() =>
    // id is here Place.id!
    projectPlaces.value.reduce((map, obj) => {
      map.set(obj.place.id, obj.place);
      return map;
    }, new Map())
  );

  const contacts = computed<Contact[]>(() => {
    const contacts: Contact[] = [];

    educationPlaces.value.forEach((obj) => {
      if (!obj.contacts || !obj.contacts.length || !placeMapForProject.value.has(obj.place.id)) {
        return;
      }

      obj.contacts.forEach((contact) => {
        const existingContact = contacts.find((c) => c.id === contact.id);
        if (existingContact) {
          existingContact.places?.push(obj.place);
        } else {
          contacts.push({
            ...contact,
            places: [obj.place],
          });
        }
      });
    });

    return contacts;
  });

  const internships = computed<Internship[]>(() => {
    if (!projectPlaces.value.length || !projectStudents.value.length) {
      return [];
    }

    const studentMap: Map<number, Student> = projectStudents.value.reduce((map, student) => {
      const studentObjectId = find(student.student_set, { project: { id: project.value?.id } })?.id;
      map.set(studentObjectId, student);
      return map;
    }, new Map());

    return projectInternships.value.map((obj: Internship) => {
      return {
        ...obj,
        place: placeMapForProject.value.get(obj.place) || obj.place,
        student: studentMap.get(obj.student) || obj.student,
      };
    });
  });

  async function init() {
    await fetchStudents();
    await fetchEducationPlaces();
    await fetchProjectPlaces();
    await fetchInternships();
  }

  async function fetchEducationPlaces() {
    educationPlaces.value = [];

    if (!education.value) {
      return;
    }

    await api.get(education.value.rel_places).then((res) => {
      educationPlaces.value = res.data;
    });
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
    projectStudents.value = [];

    if (!project.value) {
      return;
    }

    await api.get(project.value.rel_students).then((res) => {
      projectStudents.value = res.data;
    });
  }

  function setData(djangoEducation: Education, djangoPrograms: Program[], djangoProjects: Project[]) {
    education.value = djangoEducation;
    programs.value = djangoPrograms;
    projects.value = djangoProjects;
    selectedProjectId.value = djangoProjects[0]?.id || null;
  }

  watch(selectedProjectId, (id) => {
    if (id) {
      init();
    }
  });

  return {
    init,
    setData,
    contacts,
    internships,
    places: educationPlaces,
    programs,
    projects,
    project,
    projectPlaces,
    selectedProjectId,
    students: projectStudents,
  };
});
