import { computed, ref } from 'vue';
import { defineStore } from 'pinia';

export const useStore = defineStore('placeOffice', () => {
  const userId = ref<number>();
  const education = ref<EducationTiny>();
  const place = ref<Place>();

  function setData(djangoEducation: EducationTiny, djangoPlace: Place, djangoUserId: number) {
    userId.value = djangoUserId;
    education.value = djangoEducation;
    place.value = djangoPlace;
  }

  const admins = computed<Contact[]>(() => (place.value as Place)?.contacts.filter((contact) => contact.is_admin));
  const userIsAdmin = computed<boolean>(() => admins.value?.some((contact) => contact.user.id === userId.value));

  return {
    setData,
    education,
    place,
    admins,
    userIsAdmin,
  };
});
