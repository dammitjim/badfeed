<template>
    <div class="view-pinned">
        <div class="box" v-for="story in stories" :key="story.id">
            <div class="level">
                <div>
                    <p>{{ story.title }}</p>
                    <p>{{ story.feed.name }} - {{ story.posted }}</p>
                </div>
                <div class="field is-grouped">
                    <p class="control">
                        <a class="button">
                            <span class="icon is-small">
                                <i class="fas fa-thumbtack"></i>
                            </span>
                            <span>Pin</span>
                        </a>
                    </p>
                    <p class="control">
                        <a class="button">
                            <span class="icon is-small">
                                <i class="fas fa-archive"></i>
                            </span>
                            <span>Done</span>
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { ACTIONS } from "@/reader/store/main.js";

export default {
    name: "Pinned",
    computed: {
        stories() {
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
