import Vue from "vue";
import Vuex from "vuex";
import { Dispatch } from "vuex";
import axios from "axios";

import {
    apiDeleteEntries,
    apiDeleteEntry,
    apiPinEntry,
    apiSaveEntry,
    apiGetDashboard
} from "./api";
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
        // TODO this may be more appropriate as an object with feed ID as the key
        blocks: []
    },
    mutations: {
        pinEntry(state: IState, entry: IEntry) {
            state.pinned.push(entry);
        },
        addBlock(state: IState, newBlock: IBlock) {
            state.blocks.push(newBlock);
        },
        removeBlock(state: IState, block: IBlock) {
            state.blocks = state.blocks.filter(stateBlock => {
                return stateBlock.feed.id !== block.feed.id;
            });
        },
        removeEntry(state: IState, { feed, entry, callback }) {
            const wantedBlock = state.blocks.find(existing => {
                return existing.feed.id === feed.id;
            });
            if (wantedBlock) {
                wantedBlock.entries = wantedBlock.entries.filter(existing => {
                    return existing.id !== entry.id;
                });
                if (callback) {
                    callback(wantedBlock);
                }
            }
        },
        updateBlock(state: IState, block: IBlock) {
            const wantedBlock = state.blocks.find(existing => {
                return existing.feed.id === block.feed.id;
            });
            if (wantedBlock) {
                wantedBlock.entries = block.entries;
            }
        }
    },
    actions: {
        addBlock({ commit, state }, block: IBlock) {
            const existingBlock = state.blocks.find(eb => {
                return block.feed.id === eb.feed.id;
            });

            if (!existingBlock) {
                commit("addBlock", block);
            } else {
                commit("updateBlock", block);
            }
        },
        async archiveEntry({ commit, dispatch }, { entry, feed }) {
            await apiDeleteEntry(entry.id);
            commit("removeEntry", { feed, entry, callback: (block: IBlock) => {
                if (block.entries.length === 0) {
                    dispatch("syncBlocks");
                }
            }});
        },
        async pinEntry({ commit, dispatch }, { entry, feed }) {
            await apiPinEntry(entry.id);
            commit("pinEntry", entry);
            commit("removeEntry", { feed, entry, callback: (block: IBlock) => {
                if (block.entries.length === 0) {
                    dispatch("syncBlocks");
                }
            }});
        },
        async saveEntry({ commit, dispatch }, { entry, feed }) {
            await apiSaveEntry(entry.id);
            commit("removeEntry", { feed, entry, callback: (block: IBlock) => {
                if (block.entries.length === 0) {
                    dispatch("syncBlocks");
                }
            }});
        },
        async deleteEntries({ commit, dispatch }, { entries, feed }) {
            await apiDeleteEntries(entries.map((entry: IEntry) => entry.id));
            for (const entry of entries) {
                commit("removeEntry", { feed, entry, callback: (block: IBlock) => {
                    if (block.entries.length === 0) {
                        dispatch("syncBlocks");
                    }
                }});
            }
        },
        async syncBlocks({ dispatch }) {
            const results = await apiGetDashboard();
            for (const result of results) {
                dispatch("addBlock", result);
            }
        }
    }
});
