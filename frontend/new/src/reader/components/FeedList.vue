<template>
    <div class="feed-list">
        <b-collapse class="panel">
            <p class="panel-heading">Feeds</p>
            <div class="panel-block">
                <p class="control has-icons-left">
                    <input class="input is-small" type="text" placeholder="search" />
                    <span class="icon is-small is-left">
                        <i class="fas fa-search" aria-hidden="true"></i>
                    </span>
                </p>
            </div>
            <div class="feed-list__items">
                <FeedRow :key="feed.id" v-for="feed in feeds" :feed="feed" />
            </div>
        </b-collapse>
    </div>
</template>
<script>
import FeedRow from "@/reader/components/FeedRow";
export default {
    name: "FeedList",
    components: {
        FeedRow
    },
    mounted() {
        this.$store.dispatch("fetchFeeds");
    },
    computed: {
        feeds() {
            return this.$store.state.feeds;
        }
    }
};
</script>
<style lang="scss">
.feed-list__items {
    overflow: auto;
    max-height: 300px;
}
</style>
