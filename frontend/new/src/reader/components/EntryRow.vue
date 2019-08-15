<template>
    <div class="entry-row box">
        <div class="level">
            <div @click="toggleModal">
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
        <EntryModal :entry="entry" :open="modalOpen" ref="modal" />
    </div>
</template>
<script>
import ButtonDone from "@/reader/components/ButtonDone";
import ButtonPin from "@/reader/components/ButtonPin";
import EntryModal from "@/reader/components/EntryModal";

export default {
    name: "EntryRow",
    components: {
        ButtonDone,
        ButtonPin,
        EntryModal
    },
    props: {
        entry: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            modalOpen: false
        };
    },
    methods: {
        toggleModal() {
            this.$refs.modal.toggle();
        }
    }
};
</script>
