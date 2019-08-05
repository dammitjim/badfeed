<template>
    <div class="section">
        <div class="app container is-fluid">
            <section class="columns">
                <div class="column is-one-fifth"></div>
                <div class="column is-three-fifths">
                    <TabbedRouter />
                </div>
            </section>
            <section class="columns">
                <div class="column is-one-fifth">
                    Feeds
                </div>
                <div class="column is-three-fifths">
                    <router-view />
                </div>
            </section>
        </div>
    </div>
</template>
<script>
import TabbedRouter from "@/reader/components/TabbedRouter";

export default {
    name: "App",
    components: {
        TabbedRouter
    }
}
</script>
<style lang="scss" scoped>
@import url("../styles/views/app.scss");
</style>
