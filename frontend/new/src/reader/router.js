import Vue from "vue";
import Router from "vue-router";
import Inbox from "./views/Inbox.vue";
import Pinned from "./views/Pinned.vue";

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: "/",
            name: "inbox",
            component: Inbox
        },
        {
            path: "/pinned",
            name: "pinned",
            component: Pinned
        }
    ]
});
