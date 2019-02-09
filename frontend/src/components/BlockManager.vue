<template>
    <div>
        <Block v-bind:feed="block.feed" v-bind:entries="block.entries" v-bind:key="block.feed.id" v-for="block in blocks"/>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import { mapState } from "vuex";

import { apiGetDashboard } from "../api";
import { IState } from "../store";
import EntryBlock from "./EntryBlock.vue";
import Block from "./Block.vue";

export default Vue.extend({
    name: "BlockManager",
    components: {
        Block,
    },
    computed: mapState({
        blocks: (state: IState) => state.blocks,
    }),
    async mounted() {
        const results = await apiGetDashboard();
        for (const result of results) {
            this.$store.dispatch("addBlock", result);
        }
    },
})
</script>
