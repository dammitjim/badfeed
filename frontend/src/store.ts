import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

import { IEntry } from "./models";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

Vue.use(Vuex);

interface IState {
    pinned: IEntry[];
}

export default new Vuex.Store({
    state: {
        pinned: [],
    },
    mutations: {
        pinEntry(state: IState, entry: IEntry) {
            state.pinned.push(entry);
        },
    },
    actions: {
        pinEntry({ commit }, entry: IEntry) {
            commit("pinEntry", entry);
            const url = `/api/v1/feeds/entries/${entry.id}/`;
            axios.patch(url, { state: "pin" }, { withCredentials: true });
        },
    },
});
