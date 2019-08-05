import Vue from "vue";
import Vuex from "vuex";

import { createSpoofFeeds, createSpoofStories } from "@/reader/store/mock";

Vue.use(Vuex);

export const MUTATIONS = {
    REMOVE_STORY: "removeStory",
    PIN_STORY: "pinStory"
};

export const ACTIONS = {
    PIN_STORY: "pinStory",
    REMOVE_STORY_FROM_INBOX: "removeStoryFromInbox"
};

export const store = new Vuex.Store({
    state: {
        feeds: createSpoofFeeds(5),
        inbox: createSpoofStories(10),
        pinned: []
    },
    mutations: {
        pinStory(state, story) {
            state.pinned.push(story);
        },
        removeStory(state, story) {
            state.inbox = state.inbox.filter(s => s.id != story.id);
        }
    },
    actions: {
        async pinStory({ commit, dispatch, state }, story) {
            await dispatch(ACTIONS.REMOVE_STORY_FROM_INBOX, story);

            const alreadyPinned = state.pinned.find(s => s.id === story.id) !== undefined;
            if (!alreadyPinned) {
                commit(MUTATIONS.PIN_STORY, story);
            }
        },
        async removeStoryFromInbox({ commit }, story) {
            commit(MUTATIONS.REMOVE_STORY, story);
        }
    }
});
