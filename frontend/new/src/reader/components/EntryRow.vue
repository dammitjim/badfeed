<template>
    <div class="entry-row box">
        <div class="level">
            <div>
                <p>{{ entry.title }}</p>
                <p>{{ entry.feed.title }} - {{ entry.posted }}</p>
            </div>
            <div class="field is-grouped">
                <p class="control">
                    <ButtonPin :entry="entry" />
                </p>
            </div>
        </div>
    </div>
</template>
<script>
import ButtonPin from "@/reader/components/ButtonPin";

export default {
    name: "EntryRow",
    components: {
        ButtonPin
    },
    props: {
        entry: {
            type: Object,
            required: true
        }
    }
};
</script>
