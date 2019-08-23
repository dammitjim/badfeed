<template>
    <div :class="{'entry-row': true, 'box': true, 'expanded': expanded}">
        <div class="level">
            <div @click="expand">
                <p>{{ entry.title }}</p>
                <p>{{ entry.feed.title }} - {{ entry.posted }}</p>
            </div>
            <div class="field is-grouped">
                <p class="control">
                    <ButtonPin :entry="entry" />
                </p>
                <p class="control">
                    <ButtonDone :entry="entry" />
                </p>
            </div>
        </div>
        <div class="level" v-if="expanded">
            <img :src="entry.enriched.images[0]" />
            <div class="content" v-html="entry.enriched.summary" />
        </div>
        <div class="level" v-if="expanded">
            <a class="button-pin button" :href="entry.link" target="blank">
                <span class="icon is-small">
                    <i class="fas fa-book-open"></i>
                </span>
                <span>Continue Reading</span>
            </a>
        </div>
    </div>
</template>
<script>
import ButtonDone from "@/reader/components/ButtonDone";
import ButtonPin from "@/reader/components/ButtonPin";

export default {
    name: "EntryRow",
    components: {
        ButtonDone,
        ButtonPin
    },
    props: {
        entry: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            expanded: false,
            maximised: false
        };
    },
    methods: {
        expand() {
            this.expanded = !this.expanded;
        }
    }
};
</script>
<style lang="scss" scoped>
.expanded {
    z-index: 10;
    width: 110%;
    position: relative;
    left: -5%;
    bottom: 0.75rem;
    min-height: 200px;

    &:not(:last-child) {
        margin-bottom: 0rem;
    }
}

img {
    margin-right: 30px;
}
</style>
