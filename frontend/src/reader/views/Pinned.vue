<template>
    <div class="view-pinned">
        <EntryList :entries="entries" />
    </div>
</template>
<script>
import EntryList from "@/reader/components/EntryList";
import { ACTIONS } from "@/reader/store/main.js";

export default {
    name: "Pinned",
    components: {
        EntryList
    },
    computed: {
        entries() {
            return this.$store.state.pinned;
        }
    },
    mounted() {
        this.$store.dispatch(ACTIONS.FETCH_PINNED_ENTRIES);
    }
};
</script>
<style lang="scss" scoped>
@import url("../../styles/views/pinned.scss");
</style>
