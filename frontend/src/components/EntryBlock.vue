<template>
    <div>
        <button class="card-link" v-on:click="done(entries)">Done</button>
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

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

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
        this.loadEntries();
    },
    methods: {
        loadEntries: function () {
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
            this.entries = this.entries.filter(blockEntry => {
                return blockEntry.id != entry.id;
            });

            axios.delete(`/api/v1/feeds/entries/${entry.id}/`, {withCredentials: true});
        },
        done: function (entries) {
            axios.all(this.entries.map(entry => {
                return axios.delete(`/api/v1/feeds/entries/${entry.id}/`, {withCredentials: true});
            }))
            .then(axios.spread((acct, perms) => {
                this.loadEntries();
            }));
        }
    }
});
</script>
