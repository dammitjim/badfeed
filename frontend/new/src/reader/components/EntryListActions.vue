<template>
    <section class="entry-list-actions section">
        <a class="button" @click="done">
            <span class="icon is-small">
                <i class="fas fa-angle-down"></i>
            </span>
            <span>Done with these {{ entries.length }}.</span>
        </a>
    </section>
</template>
<script>
import { ACTIONS } from "@/reader/store/main.js";

export default {
    name: "EntryListActions",
    props: {
        entries: {
            type: Array,
            required: true
        }
    },
    methods: {
        done() {
            this.entries.forEach(e => this.$store.dispatch(ACTIONS.REMOVE_STORY_FROM_INBOX, e));
        }
    }
};
</script>

