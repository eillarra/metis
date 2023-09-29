<style lang="scss">
.metis__md-editor {
  .toastui-editor-defaultUI {
    border-radius: 0;
    border: 0px;
  }

  .toastui-editor-defaultUI-toolbar {
    padding: 0 !important;
  }

  .ProseMirror {
    background-color: #f7f9fc;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
  }

  .toastui-editor-tabs,
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

  .ProseMirror {
    height: 100%;
  }

  .toastui-editor-tabs .tab-item {
    font-size: 16px !important;
  }
}
</style>

<template>
  <div
    ref="canvas"
    class="metis__md-editor bg-white full-width"
    autocorrect="off"
    autocapitalize="off"
    spellcheck="false"
  />
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

import '@toast-ui/editor/dist/toastui-editor.css';
import Editor from '@toast-ui/editor';

const emit = defineEmits(['update:modelValue']);

const props = defineProps<{
  modelValue: string;
}>();

const canvas = ref<HTMLElement | null>(null);
const options = {
  usageStatistics: false,
  height: 'auto',
  maxHeight: '350px',
  minWidth: '100%',
  language: 'en-US',
  useCommandShortcut: true,
  hideModeSwitch: true,
  initialEditType: 'markdown',
  previewStyle: 'vertical',
  previewHighlight: false,
  toolbarItems: [['bold', 'italic', 'link'], ['ul', 'ol'], ['quote']],
};

onMounted(() => {
  const editor = new Editor({
    el: canvas.value,
    initialValue: props.modelValue,
    ...options,
  });

  editor.on('change', () => {
    emit('update:modelValue', editor.getMarkdown());
  });
});
</script>
