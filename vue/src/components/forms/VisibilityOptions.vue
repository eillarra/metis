<template>
  <div class="q-mt-sm">
    <span v-if="!hideLabel" class="text-body2">{{ $t('field.visibility') }}</span>
    <q-option-group
      v-model="visibility"
      :options="visibilityOptions"
      type="checkbox"
      dense
      color="primary"
      size="sm"
      class="q-my-sm"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  modelValue: Tags;
  options: string[];
  hideLabel?: boolean;
}>();

const { t } = useI18n();

const visibility = ref<string[]>([]);
const visibilityOptions = computed<QuasarSelectOption[]>(() => {
  return props.options.map((option) => ({
    value: option,
    label: t(`field.visibility_options.${option}`) as string,
  }));
});

watch(visibility, (val: string[], oldVal: string[]) => {
  if (val === oldVal) return;
  const tags = props.modelValue.filter((tag) => !tag.startsWith('_visible:'));
  const visibilityTags = val.map((val) => `_visible:${val}`);
  emit('update:modelValue', [...tags, ...visibilityTags]);
});
</script>
