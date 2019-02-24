<template>
  <div>
    <h4>{{ feed.title }}</h4>
    <div class="text-right mb-3">
      <button class="btn btn-success" v-on:click="done(entries)">Done</button>
    </div>
    <div v-bind:key="entry.id" v-for="entry in entries" class="card mb-3">
      <div class="card-body d-flex justify-content-between">
        <div>
          <h5 class="card-title">
            <a :href="entry.link" target="_blank">#{{ entry.iterator }} {{ entry.title }}</a>
          </h5>
        </div>
        <div class="card-actions">
          <button class="btn btn-primary mr-2" v-on:click="pin(entry)">Pin</button>
          <button class="btn btn-primary mr-2" v-on:click="save(entry)">Save</button>
          <button class="btn btn-success" v-on:click="archive(entry)">Done</button>
        </div>
      </div>
    </div>
    <hr>
    <!-- {{ remaining }} left to address. -->
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import { IBlock } from "../store";
import { IEntry } from "../models";

export default Vue.extend({
    name: "Block",
    props: ["feed", "entries"],
    methods: {
        save(entry: IEntry) {
            this.$store.dispatch("saveEntry", { entry, feed: this.$props.feed });
        },
        pin(entry: IEntry) {
            this.$store.dispatch("pinEntry", { entry, feed: this.$props.feed });
        },
        archive(entry: IEntry) {
            this.$store.dispatch("archiveEntry", {entry, feed: this.$props.feed});
        },
        done(entries: IEntry[]) {
            this.$store.dispatch("deleteEntries", {entries: this.$props.entries, feed: this.$props.feed});
        }
    }
});
</script>
