<template>
  <div v-if="visibilityTags.length" class="q-gutter-xs">
    <q-chip
      v-for="tag in visibilityTags"
      color="grey-2"
      :key="tag"
      :label="tag"
      icon="visibility"
      class="text-caption"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps<{
  tags: Tags;
}>();

const { t } = useI18n();

const visibilityTags = computed(() => {
  return props.tags
    .filter((tag: string) => tag.startsWith('_visible:'))
    .map((tag: string) => t(tag.replace('_visible:', ''), 9).toLowerCase())
    .sort((a: string, b: string) => a.localeCompare(b));
});
</script>
