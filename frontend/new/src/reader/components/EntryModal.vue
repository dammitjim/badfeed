<template>
    <b-modal :active.sync="open" :width="640">
        <div class="card">
            <div class="card-image">
                <figure class="image is-4by3">
                    <img src="https://www.fillmurray.com/g/1280/900" alt="Image" />
                </figure>
            </div>
            <div class="card-content">
                <div class="media">
                    <div class="media-left">
                        <figure class="image is-48x48">
                            <img src="https://www.fillmurray.com/g/300/300" alt="Image" />
                        </figure>
                    </div>
                    <div class="media-content">
                        <p class="title is-4">{{ entry.title }}</p>
                        <p class="subtitle is-6">@{{ entry.feed.title }}</p>
                    </div>
                </div>
                <div class="content" v-html="entry.content" />
            </div>
        </div>
    </b-modal>
</template>
<script>
import { ACTIONS } from "@/reader/store/main";
export default {
    name: "EntryModal",
    props: {
        entry: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            open: false
        }
    },
    methods: {
        toggle() {
            if (!this.open && this.entry.content === "") {
                this.$store.dispatch(ACTIONS.ENRICH_ENTRY, this.entry);
            }

            this.open = !this.open;
        }
    }
};
</script>
