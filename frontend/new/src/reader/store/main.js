import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import Cookies from "js-cookie";

import { normaliseEntry, normaliseFeed } from "@/reader/store/normalise";

Vue.use(Vuex);

export const MUTATIONS = {
    REMOVE_STORY: "removeStory",
    PIN_STORY: "pinStory",
    ADD_STORY_TO_INBOX: "addStoryToInbox"
    ADD_STORY_TO_INBOX: "addStoryToInbox",
    ADD_FEED_TO_MENU: "addFeedToMenu",
};

export const ACTIONS = {
    PIN_STORY: "pinStory",
    REMOVE_STORY_FROM_INBOX: "removeStoryFromInbox",
    FETCH_ENTRIES: "fetchEntries",
    FETCH_PINNED_ENTRIES: "fetchPinnedEntries"
};

export const store = new Vuex.Store({
    state: {
        feeds: createSpoofFeeds(20),
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
        },
        addStoryToInbox(state, story) {
            state.inbox.push(story);
        },
        addFeedToMenu(state, feed) {
            state.feeds.push(feed);
        },
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
        async removeStoryFromInbox({ commit, dispatch }, story) {
            commit(MUTATIONS.REMOVE_STORY, story);
            dispatch(ACTIONS.FETCH_ENTRIES);
        },
        async fetchEntries({ commit, state }, page = 1) {
            const response = await axios.get(`http://localhost:8000/api/v1/entries/?page=${page}`);
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
            const response = await axios.get(
                `http://localhost:8000/api/v1/entries/pinned/?page=${page}`
            );
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
        }
    }
});
