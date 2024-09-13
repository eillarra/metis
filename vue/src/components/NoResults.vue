<template>
  <div class="flex items-center">
    <svg xmlns="http://www.w3.org/2000/svg" :height="size" viewBox="0 -960 960 960" :width="size" fill="#aaa">
      <path
        d="M283-309h166v-22H283v22Zm372 0h22v-22h-22v22ZM283-469h166v-22H283v22Zm372 0h22v-182h-22v182ZM283-629h166v-22H283v22Zm-99.22 457q-22.02 0-37.9-15.88Q130-203.76 130-225.76v-508.48q0-22 15.88-37.88Q161.76-788 183.78-788h592.44q22.02 0 37.9 15.88Q830-756.24 830-734.24v508.48q0 22-15.88 37.88Q798.24-172 776.22-172H183.78Zm.22-22h592q12 0 22-10t10-22v-508q0-12-10-22t-22-10H184q-12 0-22 10t-10 22v508q0 12 10 22t22 10Zm-32 0v-572 572Z"
      />
    </svg>
    <span class="q-ml-sm text-grey-6">{{ $q.lang.table.noData }}</span>
  </div>
</template>

<script setup lang="ts">
const size = '48px';
</script>
