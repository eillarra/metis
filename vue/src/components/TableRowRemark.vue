<template>
  <q-icon :name="iconChat" class="cursor-pointer">
    <q-popup-proxy :anchor="anchor || 'bottom end'" :self="self || 'top end'">
      <q-banner dense class="bg-blue-1 text-dark text-body1">
        <template v-slot:avatar>
          <q-icon name="chat_bubble_outline" size="xs" />
        </template>
        {{ remark }}
      </q-banner>
    </q-popup-proxy>
  </q-icon>
</template>

<script setup lang="ts">
import { iconChat } from '@/icons';

defineProps<{
  remark: string;
  anchor?: string;
  self?: string;
}>();
</script>
