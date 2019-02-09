import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

import { apiDeleteEntries, apiDeleteEntry, apiPinEntry, apiSaveEntry } from "./api";
import { IEntry, IFeed } from "./models";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

Vue.use(Vuex);

export interface IBlock {
    feed: IFeed;
    entries: IEntry[];
}

export interface IState {
    pinned: IEntry[];
    blocks: IBlock[];
}

export default new Vuex.Store({
    state: {
        pinned: [],
        blocks: []
    },
    mutations: {
        pinEntry(state: IState, entry: IEntry) {
            state.pinned.push(entry);
        },
        addBlock(state: IState, newBlock: IBlock) {
            state.blocks.push(newBlock);
        },
        removeEntry(state: IState, {feed, entry}) {
            const wantedBlock = state.blocks.find(existing => {
                return existing.feed.id === feed.id;
            });
            if (wantedBlock) {
                wantedBlock.entries = wantedBlock.entries.filter(existing => {
                    return existing.id !== entry.id;
                });
            }
        },
    },
    actions: {
        addBlock({ commit, state }, block: IBlock) {
            const exists = state.blocks.some(existingBlock => {
                return block.feed.id === existingBlock.feed.id;
            });

            if (!exists) {
                commit("addBlock", block);
            }
        },
        async archiveEntry({ commit }, { entry, feed }) {
            await apiDeleteEntry(entry.id);
            commit("removeEntry", {feed, entry});
        },
        async pinEntry({ commit }, { entry, feed}) {
            await apiPinEntry(entry.id);
            commit("pinEntry", entry);
            commit("removeEntry", { entry, feed });
        },
        async saveEntry({ commit }, { entry, feed}) {
            await apiSaveEntry(entry.id);
            commit("removeEntry", { entry, feed });
        },
        async deleteEntries({ commit }, { entries, feed }) {
            await apiDeleteEntries(entries.map((entry: IEntry) => entry.id));
            for (const entry of entries) {
                commit("removeEntry", { entry, feed });
            }
        }
    }
});
