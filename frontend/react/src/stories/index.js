import React from 'react';

import { storiesOf } from '@storybook/react';
import { withKnobs, boolean } from "@storybook/addon-knobs";

import EntryRowLarge from "../components/entry-row-large/index.tsx";
import EntryRowSmall from "../components/entry-row-small/index.tsx";

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
    .add('large', () => (
        <EntryRowLarge entry={dummyEntry} important={boolean("Important", false)}/>
    ))
    .add('small', () => (
        <EntryRowSmall entry={dummyEntry} important={boolean("Important", false)}/>
    ))
