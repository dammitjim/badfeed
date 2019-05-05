/* eslint-disable import/no-extraneous-dependencies */
import {storiesOf} from '@storybook/vue'
import {withKnobs, boolean} from '@storybook/addon-knobs'

import EntryRow from "../components/EntryRow.vue"

const dummyEntry = {
    title: "'League of Legends' Studio Faces Employee Walkout, Promises Changes",
    summary: "Riot Games' decision to try and block lawsuits being filed against the company prompted an enormous internal blowback it's still wrestling with.",
    href: "https://tightenupthe.tech",
    feed: {title: "Waypoint", href: "https://tightenupthe.tech"},
    relativeDatePublished: "2 days ago",
};

const entryRowStories = storiesOf("EntryRow", module);
entryRowStories.addDecorator(withKnobs);
entryRowStories
    .add("regular", () => ({
        components: {EntryRow},
        template: '<EntryRow :entry="entry" :detailed="detailed" :important="important" />',
        props: {
            entry: {default: dummyEntry},
            detailed: {default: boolean("Detailed", true)},
            important: {default: boolean("Important", false)},
        }
    }))
