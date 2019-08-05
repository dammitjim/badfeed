<template>
  <b-tabs type="is-boxed" @change="handleClick">
    <b-tab-item label="Inbox" icon="paper-plane"></b-tab-item>
    <b-tab-item label="Pinned" icon="thumbtack"></b-tab-item>
  </b-tabs>
</template>
<script>
const indexToRouteMap = {
    0: { path: "/" },
    1: { path: "pinned" }
};

// TODO: calculate starting index based on current route
export default {
    name: "TabbedRouter",
    methods: {
        /**
         * Navigate to the corresponding route based on the
         * tab index.
         *
         * @param {Integer} index
         */
        handleClick(index) {
            const routeProps = indexToRouteMap[index];
            this.$router.push(routeProps);
        }
    }
};
</script>

