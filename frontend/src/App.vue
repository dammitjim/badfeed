<template>
  <div id="app">
    <EntryBlock />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import EntryBlock from "./components/EntryBlock.vue";

export default Vue.extend({
  name: 'app',
  components: {
    EntryBlock,
  },
});
</script>
