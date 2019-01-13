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

const removeEntry = (id, entries): [] => {
    return entries.filter(entry => {
        return id != entry.id;
    });
};

const buildStateURL = (id): [] => {
    return `/api/v1/feeds/entries/${id}/`;
}

export default Vue.extend({
    name: "EntryBlock",
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
        patchEntryState: function (id, state) {
            this.entries = removeEntry(id, this.entries);
            const url = buildStateURL(id);
            axios.patch(url, {state}, {withCredentials: true});
        },
        save: function (entry) {
            this.patchEntryState(entry.id, "save");
        },
        pin: function (entry) {
            this.patchEntryState(entry.id, "pin");
        },
        archive: function (entry) {
            this.entries = this.entries.filter(blockEntry => {
                return blockEntry.id != entry.id;
            });

            const url = buildStateURL(entry.id);
            axios.delete(url, {withCredentials: true});
        },
        done: function (entries) {
            axios.all(this.entries.map(entry => {
                const url = buildStateURL(entry.id);
                return axios.delete(url, {withCredentials: true});
            }))
            .then(axios.spread((acct, perms) => {
                this.loadEntries();
            }));
        }
    }
});
</script>
