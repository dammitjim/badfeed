<template>
  <div>
    <div class="text-right mb-3">
      <button class="btn btn-success" v-on:click="done(entries)">Done</button>
    </div>
    <div v-bind:key="entry.id" v-for="entry in entries" class="card mb-3">
      <div class="card-body d-flex justify-content-between">
        <div>
          <h5 class="card-title">
            <a :href="entry.link" target="_blank">#{{ entry.iterator }} {{ entry.title }}</a>
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ entry.feed.title }}</h6>
        </div>
        <div class="card-actions">
          <button class="btn btn-primary mr-2" v-on:click="pin(entry)">Pin</button>
          <button class="btn btn-primary mr-2" v-on:click="save(entry)">Save</button>
          <button class="btn btn-success" v-on:click="archive(entry)">Done</button>
        </div>
      </div>
    </div>
    <hr>
    {{ remaining }} left to address.
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";

import { IEntry } from "../models";
import { deleteEntries, deleteEntry, pinEntry, saveEntry } from "../api";

const removeEntry = (
    id: number,
    entries: IEntryExtended[]
): IEntryExtended[] => {
    return entries.filter(entry => {
        return id !== entry.id;
    });
};

const buildStateURL = (id: number): string => {
    return `/api/v1/feeds/entries/${id}/`;
};

interface IEntryExtended extends IEntry {
    iterator: number;
}

interface IData {
    entries: IEntryExtended[];
    remaining: number;
}

export default Vue.extend({
    name: "EntryBlock",
    data(): IData {
        return {
            entries: [],
            remaining: 0
        };
    },
    mounted() {
        this.loadEntries();
    },
    methods: {
        loadEntries() {
            axios.get("/api/v1/feeds/entries/unread/").then(response => {
                let iter = 1;
                this.entries = response.data.results.map(
                    (entry: IEntryExtended) => {
                        entry.iterator = iter;
                        iter += 1;
                        return entry;
                    }
                );
                this.remaining = response.data.count;
            });
        },
        save(entry: IEntry) {
            this.entries = removeEntry(entry.id, this.entries);
            saveEntry(entry.id);
        },
        pin(entry: IEntry) {
            this.entries = removeEntry(entry.id, this.entries);
            pinEntry(entry.id);
        },
        archive(entry: IEntry) {
            this.entries = this.entries.filter(blockEntry => {
                return blockEntry.id !== entry.id;
            });
            deleteEntry(entry.id);
        },
        done(entries: IEntry[]) {
            deleteEntries(this.entries.map(entry => entry.id))
                .then(response => {
                    this.loadEntries();
                });
        }
    }
});
</script>
