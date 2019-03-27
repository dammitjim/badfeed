<template>
    <div id="app"><BlockManager /></div>
</template>

<script lang="ts">
import Vue from "vue";
import BlockManager from "./components/BlockManager.vue";

export default Vue.extend({
    name: "app",
    components: {
        BlockManager,
    },
});
</script>
