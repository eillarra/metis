import { computed, ref, watch } from 'vue';
import { defineStore } from 'pinia';
import { cloneDeep } from 'lodash-es';

import { api } from '@/axios.ts';

export const useStore = defineStore('educationOffice', () => {
  const education = ref<Education | null>(null);
  const emails = ref<Email[]>([]);
  const programs = ref<Program[]>([]);
  const projects = ref<Project[]>([]);
  const projectInternships = ref<Internship[]>([]);
  const projectPlaces = ref<ProjectPlace[]>([]);
  const questionings = ref<Questioning[]>([]);
  const students = ref<StudentUser[]>([]);

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
              Block: block,
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
      period.ProgramInternship = programInternshipMap.value.get(period.program_internship);
      return period;
    });

    return selectedProject;
  });

  const projectStudents = computed<Student[]>(() => {
    if (!selectedProjectId.value || !students.value.length) {
      return [];
    }

    return students.value.reduce((arr, studentUser) => {
      studentUser.student_set
        .filter((student) => student.project === selectedProjectId.value)
        .forEach((student) => {
          arr.push({
            ...student,
            User: {
              ...studentUser,
              student_set: [], // just make the object smaller
            } as StudentUser,
          });
        });
      return arr;
    }, [] as Student[]);
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
            Place: {
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
      set.add(obj.student as number);
      return set;
    }, new Set<number>());
  });

  const projectPlaceMap = computed<Map<number, Place>>(() =>
    projectPlaces.value.reduce((map, obj) => {
      map.set(obj.id, obj.place);
      return map;
    }, new Map())
  );

  const disciplineMap = computed<Map<number, Discipline>>(
    () =>
      education.value?.disciplines.reduce((map, discipline) => {
        map.set(discipline.id, discipline);
        return map;
      }, new Map()) || new Map()
  );

  const blockMap = computed<Map<number, Track>>(() =>
    programs.value.reduce((map, program) => {
      program.blocks.forEach((block) => {
        map.set(block.id, block);
      });
      return map;
    }, new Map())
  );

  const trackMap = computed<Map<number, Track>>(() =>
    programs.value.reduce((map, program) => {
      program.tracks.forEach((track) => {
        map.set(track.id, track);
      });
      return map;
    }, new Map())
  );

  const periodMap = computed<Map<number, Period>>(() => {
    if (!project.value) {
      return new Map();
    }

    return project.value.periods.reduce((map, period) => {
      map.set(period.id, period);
      return map;
    }, new Map());
  });

  const projectMap = computed<Map<number, Project>>(() =>
    projects.value.reduce((map, project) => {
      map.set(project.id, project);
      return map;
    }, new Map())
  );

  const studentMap = computed<Map<number, Student>>(() =>
    students.value.reduce((map, studentUser) => {
      studentUser.student_set
        .filter((student) => student.project === selectedProjectId.value)
        .forEach((student) => {
          map.set(student.id, {
            ...student,
            User: {
              ...studentUser,
              student_set: [], // just make the object smaller
            } as StudentUser,
          } as Student);
        });
      return map;
    }, new Map())
  );

  const internships = computed<Internship[]>(() => {
    if (!project.value || !students.value.length) {
      return [];
    }

    return projectInternships.value.map((obj: Internship) => ({
      ...obj,
      // -----
      tag_objects: obj.tags.reduce((dict, tag) => {
        const parts = tag.split(':');
        const value = parts.slice(1).join(':');
        dict[parts[0]] = value.replace(/"/g, '');
        return dict;
      }, {} as { [tag: string]: string }),
      // -----
      Student: studentMap.value.get(obj.student as number) || undefined,
      Track: trackMap.value.get(obj.track as number) || undefined,
      Period: periodMap.value.get(obj.period as number) || undefined,
      Discipline: disciplineMap.value.get(obj.discipline as number) || undefined,
      Place: projectPlaceMap.value.get(obj.project_place) || undefined,
    }));
  });

  async function init() {
    await fetchStudents();
    await fetchProjectPlaces();
    await fetchInternships();
  }

  async function fetchEmails() {
    emails.value = [];

    if (!project.value) {
      return;
    }

    await api.get(project.value.rel_emails).then((res) => {
      emails.value = res.data.map((obj: Email) => {
        obj.tag_set = new Set(obj.tags);
        return obj;
      });
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

    const placeTypeMap =
      education.value?.place_types.reduce((map, placeType) => {
        map.set(placeType.id, placeType);
        return map;
      }, new Map()) || new Map();

    await api.get(project.value.rel_places).then((res) => {
      projectPlaces.value = res.data.map((obj: ProjectPlace) => {
        obj.place.Type = placeTypeMap.get(obj.place.type as number) || undefined;
        return {
          ...obj,
          Disciplines: obj.disciplines.map((id: number) => disciplineMap.value.get(id)),
          _periods: obj.availability_set.reduce((set, availability) => {
            if (availability.min > 0) {
              set.add(availability.period);
            }
            return set;
          }, new Set<number>()),
        };
      });
    });
  }

  async function fetchQuestionings() {
    questionings.value = [];

    if (!project.value) {
      return;
    }

    await api.get(project.value.rel_questionings).then((res) => {
      questionings.value = res.data.map(
        (obj: Questioning) =>
          ({
            ...obj,
            Period: periodMap.value.get(obj.period as number) || undefined,
          } as Questioning)
      );
    });
  }

  async function fetchStudents() {
    students.value = [];

    if (!project.value) {
      return;
    }

    const projectIds = projects.value.reduce((set, project) => {
      set.add(project.id);
      return set;
    }, new Set<number>());

    await api.get(project.value.rel_students).then((res) => {
      students.value = res.data.map(
        (obj: StudentUser) =>
          ({
            ...obj,
            student_set: obj.student_set
              .filter((student: Student) => projectIds.has(student.project as number))
              .map(
                (student: Student) =>
                  ({
                    ...student,
                    Project: projectMap.value.get(student.project as number),
                    Track: trackMap.value.get(student.track as number),
                    Block: blockMap.value.get(student.block as number),
                  } as Student)
              ),
          } as StudentUser)
      );
    });
  }

  function setData(djangoEducation: Education, djangoPrograms: Program[], djangoProjects: Project[]) {
    education.value = djangoEducation;
    programs.value = djangoPrograms;
    projects.value = djangoProjects.sort((a, b) => {
      return new Date(b.start_date).getTime() - new Date(a.start_date).getTime();
    });
    selectedProjectId.value = djangoProjects[0]?.id || null;
  }

  function updateCollection(type: string, action: string, obj: ApiObject) {
    let collection: ApiObject[] = [];

    switch (type) {
      case 'contact':
        collection = places.value.find((row) => row.id === (obj as Contact).place)?.contacts as Contact[];
        break;
      case 'projectInternship':
        collection = projectInternships.value as Internship[];
        break;
      case 'projectPlace':
        collection = projectPlaces.value as ProjectPlace[];
        break;
      case 'questioning':
        collection = questionings.value as Questioning[];
        break;
      case 'student':
        if (action == 'insert') {
          fetchStudents();
          return;
        }
        collection = students.value as StudentUser[];
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
      fetchEmails();
    }
  });

  return {
    init,
    fetchEmails,
    fetchQuestionings,
    setData,
    createObj,
    updateObj,
    deleteObj,
    education,
    contacts,
    emails,
    internships,
    places,
    programs,
    projects,
    project,
    projectPlaces,
    projectPlacesWithInternships,
    projectStudents,
    projectStudentsWithInternships,
    questionings,
    selectedProjectId,
    students,
    blockMap,
    disciplineMap,
    projectMap,
    trackMap,
  };
});
