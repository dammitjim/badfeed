import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import Cookies from "js-cookie";

import { normaliseEntry, normaliseFeed } from "@/reader/store/normalise";

Vue.use(Vuex);

export const MUTATIONS = {
    REMOVE_STORY: "removeStory",
    PIN_STORY: "pinStory",
    ADD_STORY_TO_INBOX: "addStoryToInbox",
    ADD_FEED_TO_MENU: "addFeedToMenu",
    REPLACE_ENTRY: "replaceEntry"
};

export const ACTIONS = {
    PIN_STORY: "pinStory",
    FETCH_ENTRIES: "fetchEntries",
    FETCH_PINNED_ENTRIES: "fetchPinnedEntries",
    ENRICH_ENTRY: "enrichEntry",
    MARK_AS_DONE: "markAsDone",
    DONE_WITH_ENTRY: "doneWithEntry",
    FETCH_FEEDS: "fetchFeeds"
};

// TODO: refactor basically all of this, so much code reuse
export const store = new Vuex.Store({
    state: {
        feeds: [],
        inbox: [],
        pinned: []
    },
    mutations: {
        pinStory(state, story) {
            state.pinned.push(story);
        },
        removeStory(state, story) {
            state.inbox = state.inbox.filter(s => s.id != story.id);
            state.pinned = state.pinned.filter(s => s.id != story.id);
        },
        addStoryToInbox(state, story) {
            state.inbox.push(story);
        },
        addFeedToMenu(state, feed) {
            state.feeds.push(feed);
        },
        replaceEntry(state, entry) {
            let index = state.inbox.findIndex(item => {
                return item.id === entry.id;
            });
            if (index) {
                state.inbox = [
                    ...state.inbox.slice(0, index),
                    entry,
                    ...state.inbox.slice(index + 1)
                ];
            } else {
                index = state.inbox.findIndex(item => {
                    return item.id === entry.id;
                });
                state.pinned = [
                    ...state.pinned.slice(0, index),
                    entry,
                    ...state.pinned.slice(index + 1)
                ];
            }
        }
    },
    actions: {
        async pinStory({ commit, dispatch, state }, story) {
            await commit(MUTATIONS.REMOVE_STORY, story);

            const alreadyPinned = state.pinned.find(s => s.id === story.id) !== undefined;
            if (!alreadyPinned) {
                const csrf = Cookies.get("csrftoken");
                const response = await axios.post(
                    `http://localhost:8000/api/v1/states/`,
                    {
                        actions: [
                            {
                                state: "pinned",
                                entry_id: story.id
                            }
                        ]
                    },
                    { headers: { "X-CSRFTOKEN": csrf } }
                );

                if (response.status !== 200) {
                    throw "Non 200 response status received from API";
                }

                commit(MUTATIONS.PIN_STORY, story);
            }

            await dispatch(ACTIONS.FETCH_ENTRIES);
        },
        async doneWithEntry({ dispatch }, entry) {
            await dispatch(ACTIONS.MARK_AS_DONE, [entry]);
        },
        async fetchEntries({ commit, state }, page = 1) {
            const response = await axios.get(`/api/v1/entries/?page=${page}`);
            if (response.status !== 200) {
                throw "Non 200 response status received from API";
            }

            const entries = response.data.results.map(normaliseEntry);
            entries.forEach(entry => {
                if (state.inbox.find(e => e.id === entry.id) !== undefined) {
                    return;
                }
                commit(MUTATIONS.ADD_STORY_TO_INBOX, entry);
            });
        },
        async fetchPinnedEntries({ commit, state }, page = 1) {
            const response = await axios.get(`/api/v1/entries/pinned/?page=${page}`);
            if (response.status !== 200) {
                throw "Non 200 response status received from API";
            }

            const entries = response.data.results.map(normaliseEntry);
            entries.forEach(entry => {
                if (state.pinned.find(e => e.id === entry.id) !== undefined) {
                    return;
                }

                commit(MUTATIONS.PIN_STORY, entry);
            });
        },
        async fetchFeeds({ commit, state }, page = 1) {
            const response = await axios.get(`/api/v1/feeds/?only_watched=true&page=${page}`);
            if (response.status !== 200) {
                throw "Non 200 response status received from API";
            }

            const feeds = response.data.results.map(normaliseFeed);
            feeds.forEach(feed => {
                if (state.feeds.find(f => f.id === feed.id) !== undefined) {
                    return;
                }

                commit(MUTATIONS.ADD_FEED_TO_MENU, feed);
            });
        },
        async enrichEntry({ commit }, entry) {
            const response = await axios.get(`/api/v1/entries/${entry.id}`);
            if (response.status !== 200) {
                throw "Non 200 response status received from API";
            }
            entry.content = response.data.content;
            commit(MUTATIONS.REPLACE_ENTRY, entry);
        },
        async markAsDone({ commit, dispatch }, entries) {
            const actions = entries.map(entry => {
                return {
                    state: "deleted",
                    entry_id: entry.id
                };
            });
            const csrf = Cookies.get("csrftoken");
            const response = await axios.post(
                `/api/v1/states/`,
                { actions },
                {
                    headers: { "X-CSRFTOKEN": csrf }
                }
            );
            if (response.status !== 200) {
                throw "Non 200 response status received from API";
            }
            entries.forEach(entry => commit(MUTATIONS.REMOVE_STORY, entry));
            dispatch(ACTIONS.FETCH_ENTRIES);
            dispatch(ACTIONS.FETCH_FEEDS);
        }
    }
});
