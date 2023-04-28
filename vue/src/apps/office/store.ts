import { computed, ref, Ref } from 'vue';
import { defineStore } from 'pinia';

export const useOfficeStore = defineStore('office', () => {
  const programs: Ref<Program[] | null> = ref(null);
  const projects: Ref<Project[] | null> = ref(null);
  const selectedProject: Ref<number | null> = ref(null);

  const project = computed(() => {
    return projects.value?.find((p) => p.id === selectedProject.value) || null;
  });

  function setPrograms(data: Program[]) {
    programs.value = data;
  }

  function setProjects(data: Project[]) {
    projects.value = data;
    selectedProject.value = data[0].id || null;
  }

  return {
    setPrograms,
    setProjects,
    programs,
    projects,
    project,
    selectedProject,
  };
});
