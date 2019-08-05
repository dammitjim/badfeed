<template>
    <a class="button-pin button" @click="pin">
        <span class="icon is-small">
            <i class="fas fa-thumbtack"></i>
        </span>
        <span>Pin</span>
    </a>
</template>
<script>
import { ACTIONS } from "@/reader/store/main.js";

export default {
    name: "ButtonPin",
    props: {
        entry: {
            type: Object,
            required: true
        }
    },
    methods: {
        async pin() {
            await this.$store.dispatch(ACTIONS.PIN_STORY, this.entry)
        }
    }
}
</script>

