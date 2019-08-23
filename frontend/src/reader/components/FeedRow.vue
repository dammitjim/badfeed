<template>
    <a class="panel-block feed-row">
        <span class="panel-icon">
            <i class="fas fa-book" aria-hidden="true"></i>
        </span>
        {{ feed.title }}
        <span v-if="feed.unread > 0"> - {{ feed.unread }}</span>
    </a>
</template>
<script>
export default {
    name: "FeedRow",
    props: {
        feed: {
            type: Object,
            required: true
        }
    }
};
</script>
