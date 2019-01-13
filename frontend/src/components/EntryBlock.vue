<template>
    <div>
        <div v-bind:key="entry.id" v-for="entry in entries" class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">
                    <a
                        :href="entry.link"
                        target="_blank"
                    >
                        #{{ entry.iterator }}
                        {{ entry.title }}
                    </a>
                </h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ entry.feed.title }}</h6>
                <hr />
                <button href="#" class="card-link" v-on:click="pin(entry)">Pin</button>
                <button href="#" class="card-link" v-on:click="save(entry)">Save</button>
                <button href="#" class="card-link" v-on:click="archive(entry)">Archive</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios';

export default Vue.extend({
    name: "EntryBlock",
    props: {
    },
    data () {
        return {
            entries: []
        };
    },
    mounted () {
        axios.get("/api/v1/feeds/entries/unread/")
            .then(response => {
                let iter = 1;
                this.entries = response.data.results.map(entry => {
                    entry.iterator = iter;
                    iter += 1;
                    return entry;
                })
            });
    },
    methods: {
        save: function (entry) {
            console.log("save");
            console.log(entry);
            this.entries = this.entries.filter(blockEntry => {
                return blockEntry.id != entry.id;
            });
        },
        pin: function (entry) {
            console.log("pin");
            console.log(entry);
            this.entries = this.entries.filter(blockEntry => {
                return blockEntry.id != entry.id;
            });
        },
        archive: function (entry) {
            console.log("archive");
            console.log(entry);
            this.entries = this.entries.filter(blockEntry => {
                return blockEntry.id != entry.id;
            });
        }
    }
});
</script>
