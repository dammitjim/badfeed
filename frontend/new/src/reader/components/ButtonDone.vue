<template>
    <a class="button-pin button" @click="done">
        <span class="icon is-small">
            <i class="fas fa-archive"></i>
        </span>
        <span>Done</span>
    </a>
</template>
<script>
import { ACTIONS } from "@/reader/store/main.js";

export default {
    name: "ButtonDone",
    props: {
        entry: {
            type: Object,
            required: true
        }
    },
    methods: {
        async done() {
            await this.$store.dispatch(ACTIONS.DONE_WITH_ENTRY, this.entry);
        }
    }
};
</script>

