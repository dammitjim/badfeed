<template>
  <div class="view-inbox">
      <EntryList :entries="entries" />
  </div>
</template>
<script>
import EntryList from "@/reader/components/EntryList";

import { ACTIONS } from "@/reader/store/main.js";

export default {
    name: "Inbox",
    components: {
        EntryList,
    },
    computed: {
        entries() {
            return this.$store.state.inbox;
        }
    },
    methods: {
        async pin(story) {
            await this.$store.dispatch(ACTIONS.PIN_STORY, story)
        }
    }
};
</script>
<style lang="scss" scoped>
@import url("../../styles/views/inbox.scss");
</style>
