<template>
    <a class="panel-block feed-row">
        <span class="panel-icon">
            <i class="fas fa-book" aria-hidden="true"></i>
        </span>
        {{ title }}
    </a>
</template>
<script>
export default {
    name: "FeedRow",
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>
