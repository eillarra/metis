<template>
  <div class="metis__form">
    <q-input v-model="updatedAt" dense :label="$t('field.updated_at')" readonly />
    <div v-if="obj.updated_by" class="q-mt-sm q-gutter-sm">
      <q-input v-model="obj.updated_by.name" dense :label="$t('field.updated_by')" readonly />
      <q-input v-model="obj.updated_by.email" dense :label="$t('field.email')" readonly>
        <template #append>
          <a @click.stop :href="`mailto:${obj.updated_by.email}`" target="_blank" class="inherit">
            <q-icon name="email" size="xs" />
          </a>
          <a
            v-if="obj.updated_by.email.includes('@ugent.be')"
            @click.stop
            :href="`https://teams.microsoft.com/l/chat/0/0?users=${obj.updated_by.email}`"
            target="_blank"
            class="q-ml-md inherit"
          >
            <q-icon :name="biMicrosoftTeams" size="xs" />
          </a>
        </template>
      </q-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { date } from 'quasar';

import { biMicrosoftTeams } from '@quasar/extras/bootstrap-icons';

const props = defineProps<{
  obj: object;
}>();

const obj = ref<ApiObjectUpdated>(props.obj as ApiObjectUpdated);
const updatedAt = computed(() => date.formatDate(obj.value.updated_at, 'YYYY-MM-DD HH:mm:ss'));
</script>
