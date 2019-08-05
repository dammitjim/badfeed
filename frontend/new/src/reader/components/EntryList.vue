<template>
  <div class="entry-list">
    <transition-group name="entry-list-transition">
      <EntryRow v-for="entry in entries" :key="entry.id" :entry="entry" />
    </transition-group>
  </div>
</template>
<script>
import EntryRow from "@/reader/components/EntryRow";
export default {
    name: "EntryList",
    components: {
        EntryRow
    },
    props: {
        entries: {
            type: Array,
            required: true
        }
    }
};
</script>
<style lang="scss">
@import url("../../styles/components/EntryList.scss");
</style>


