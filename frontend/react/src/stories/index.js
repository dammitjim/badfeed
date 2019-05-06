import React from 'react';

import { storiesOf } from '@storybook/react';
import { withKnobs, boolean } from "@storybook/addon-knobs";

import EntryRow from "../components/entry-row/index.tsx";

const dummyEntry = {
    title: "'League of Legends' Studio Faces Employee Walkout, Promises Changes",
    summary: "Riot Games' decision to try and block lawsuits being filed against the company prompted an enormous internal blowback it's still wrestling with.",
    href: "https://tightenupthe.tech",
    feed: {title: "Waypoint", href: "https://tightenupthe.tech"},
    relativeDatePublished: "2 days ago",
};

const entryRowStories = storiesOf('EntryRow', module)
entryRowStories.addDecorator(withKnobs);
entryRowStories
    .add('regular', () => (
        <EntryRow entry={dummyEntry} detailed={boolean("Disabled", true)} important={boolean("Important", false)}/>
    ))