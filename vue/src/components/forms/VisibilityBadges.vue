<template>
  <div v-if="visibilityTags.length" class="q-gutter-xs">
    <q-badge
      v-for="tag in visibilityTags"
      outline
      :key="tag"
      :icon="iconEye"
      :ripple="false"
      dense
      color="grey-8"
      class="text-caption"
    >
      <q-icon :name="iconEye" class="q-mr-xs" />{{ tag }}
    </q-badge>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { iconEye } from '@/icons';

const props = defineProps<{
  tags: Tags;
}>();

const { t } = useI18n();

const visibilityTags = computed(() => {
  return props.tags
    .filter((tag: string) => tag.startsWith('_visible:'))
    .map((tag: string) => t(tag.replace('_visible:', '')).toLowerCase())
    .sort((a: string, b: string) => a.localeCompare(b));
});
</script>
