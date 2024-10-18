<style lang="scss">
.metis__md-viewer {
  .toastui-editor-defaultUI {
    border-radius: 0;
    border: 0px;
  }

  .toastui-editor-contents {
    font-family: 'UGent Panno SemiLight', 'Arial', sans-serif;
    font-size: 18px !important;
    line-height: 1.4;
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .toastui-editor-contents :not(table) {
    line-height: inherit;
  }

  .toastui-editor-contents ul > li::before,
  .toastui-editor-contents ol > li::before {
    color: inherit;
  }

  .toastui-editor-contents ul > li::before {
    margin-top: 10px;
    background-color: #222;
  }
}
</style>

<template>
  <div ref="canvas" class="metis__md-viewer bg-white full-width" />
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';

import '@toast-ui/editor/dist/toastui-editor-viewer.css';
import Viewer from '@toast-ui/editor/dist/toastui-editor-viewer';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  modelValue: string;
  sourceText?: string;
  data?: Record<string, unknown>;
}>();

const replacedText = computed<string>(() => {
  if (!props.sourceText) return '';
  return props.data ? replaceHandlebars(props.sourceText, props.data) : props.sourceText;
});

const viewer = ref<Viewer | null>(null);
const canvas = ref<HTMLElement | null>(null);
const options = {
  usageStatistics: false,
  minWidth: '100%',
};

onMounted(() => {
  emit('update:modelValue', replacedText.value);
  viewer.value = new Viewer({
    el: canvas.value,
    initialValue: replacedText.value,
    ...options,
  });
});

function replaceHandlebars(text: string, data: Record<string, unknown>) {
  // search for handlebar coincidences and replace with values from the data object
  return text.replace(/{{([^{}]+)}}/g, (match, p1) => {
    const keys = p1.trim().split('.');
    let value = data;
    for (const key of keys) {
      value = value[key];
      if (!value) {
        break;
      }
    }
    return value ? value : match;
  });
}

watch(replacedText, (val) => {
  viewer.value?.setMarkdown(val);
  emit('update:modelValue', val);
});
</script>
