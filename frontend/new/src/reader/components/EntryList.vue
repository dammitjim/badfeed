<template>
    <div class="entry-list">
        <EntryRow v-for="entry in entries" :key="entry.id" :entry="entry" />
        <EntryListActions :entries="entries" />
    </div>
</template>
<script>
import EntryRow from "@/reader/components/EntryRow";
import EntryListActions from "@/reader/components/EntryListActions"
export default {
    name: "EntryList",
    components: {
        EntryRow,
        EntryListActions
    },
    props: {
        entries: {
            type: Array,
            required: true
        }
    }
};
</script>
<style lang="scss">
@import url("../../styles/components/EntryList.scss");
</style>


