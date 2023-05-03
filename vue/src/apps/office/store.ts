import { computed, ref, watch } from 'vue';
import { defineStore } from 'pinia';

import { api } from '@/axios.ts';
import { find } from 'lodash-es';

export const useOfficeStore = defineStore('office', () => {
  const programs = ref<Program[]>([]);
  const projects = ref<Project[]>([]);
  const projectInternships = ref<Internship[]>([]);
  const projectPlaces = ref<Place[]>([]);
  const projectStudents = ref<Student[]>([]);

  const selectedProjectId = ref<number | null>(null);

  const project = computed<Project | null>(() => {
    return projects.value?.find((p) => p.id === selectedProjectId.value) || null;
  });

  const contacts = computed<Contact[]>(() => {
    const contacts: Contact[] = [];

    projectPlaces.value.forEach((place) => {
      place.contacts.forEach((contact) => {
        const existingContact = contacts.find((c) => c.id === contact.id);
        if (existingContact) {
          existingContact.institutions?.push(place.institution);
        } else {
          contacts.push({
            ...contact,
            institutions: [place.institution],
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

    const placeMap: Map<number, Place> = projectPlaces.value.reduce((map, place) => {
      map.set(place.id, place);
      return map;
    }, new Map());

    const studentMap: Map<number, Student> = projectStudents.value.reduce((map, student) => {
      const studentObjectId = find(student.student_objects, { project: { id: project.value?.id } })?.id;
      map.set(studentObjectId, student);
      return map;
    }, new Map());

    return projectInternships.value.map((internship: Internship) => {
      return {
        ...internship,
        place: placeMap.get(internship.place) || internship.place,
        student: studentMap.get(internship.student) || internship.student,
      };
    });
  });

  async function init() {
    await fetchStudents();
    await fetchPlaces();
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

  async function fetchPlaces() {
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

  function setPrograms(data: Program[]) {
    programs.value = data;
  }

  function setProjects(data: Project[]) {
    projects.value = data;
    selectedProjectId.value = data[0].id || null;
  }

  watch(selectedProjectId, (id) => {
    if (id) {
      init();
    }
  });

  return {
    init,
    setPrograms,
    setProjects,
    programs,
    projects,
    project,
    selectedProjectId,
    contacts,
    internships,
    places: projectPlaces,
    students: projectStudents,
  };
});
