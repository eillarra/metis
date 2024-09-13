import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import { cloneDeep } from 'lodash-es';

import { tags_to_dict } from '@/utils/tags.ts';

interface ProjectOptions {
  value: number;
  label: string;
}

export const useStore = defineStore('placeOffice', () => {
  const userId = ref<number>();
  const education = ref<EducationTiny>();
  const internships = ref<Internship[]>([]);
  const projects = ref<Project[]>([]);
  const projectPlaces = ref<ProjectPlaceTiny[]>([]);
  const place = ref<Place>();

  const selectedProjectId = ref<number | null>(null);
  const availableProjects = ref<ProjectOptions[]>([]);

  function setData(
    djangoEducation: EducationTiny,
    djangoProjects: Project[],
    djangoPlace: Place,
    djangoProjectPlaces: ProjectPlaceTiny[],
    djangoInternships: Internship[],
    djangoUserId: number,
  ) {
    djangoProjects.sort((a, b) => {
      return new Date(b.start_date).getTime() - new Date(a.start_date).getTime();
    });
    userId.value = djangoUserId;
    education.value = djangoEducation;
    place.value = djangoPlace;
    projectPlaces.value = djangoProjectPlaces.map((projectPlace) => ({
      ...projectPlace,
      Place: djangoPlace,
    }));
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
    internships.value = djangoInternships.map((internship) => ({
      ...internship,
      // -----
      Place: djangoPlace,
      // -----
      _tags_dict: tags_to_dict(internship.tags),
    }));
    availableProjects.value = djangoProjects.map((project) => ({
      value: project.id,
      label: project.name,
    }));
    selectedProjectId.value = djangoProjects[0]?.id || null;
  }

  const admins = computed<Contact[]>(() => (place.value as Place)?.contacts.filter((contact) => contact.is_admin));
  const userIsAdmin = computed<boolean>(() => admins.value?.some((contact) => contact.user.id === userId.value));

  const project = computed<Project | undefined>(() => {
    return projects.value.find((p: Project) => p.id === selectedProjectId.value);
  });

  const projectPlace = computed<ProjectPlaceTiny | undefined>(() => {
    return projectPlaces.value.find((pp: ProjectPlaceTiny) => pp.project === selectedProjectId.value);
  });

  const projectPlacePeriodIds = computed<number[]>(() => {
    return (
      projectPlace.value?.availability_set
        .filter((availability) => availability.min > 0)
        .map((availability) => {
          return availability.period;
        }) || []
    );
  });

  const activeQuestionings = computed<Questioning[]>(() => {
    const validTypes: string[] = ['project_place_availability', 'project_place_information'];
    return (
      project.value?.questionings.filter(
        (date) =>
          date.is_active &&
          validTypes.includes(date.type) &&
          (!date.period || projectPlacePeriodIds.value.includes(date.period)),
      ) ?? []
    );
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
    setData,
    updateObj,
    education,
    internships,
    project,
    projectPlace,
    place,
    admins,
    availableProjects,
    userIsAdmin,
    activeQuestionings,
  };
});
