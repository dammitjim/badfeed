import React, {useState} from "react";

import EntryRowActions from "../entry-row-actions/index";
import EntryRowText from "../entry-row-text/index";
import FeedLink from "../feed-link/index";

import Props from "./props";

export default (props: Props) => {
    const [showActions, setShowActions] = useState(false);

    const handleMouseEnter = (event: React.MouseEvent) => {
        setShowActions(true);
    };

    const handleMouseLeave = (event: React.MouseEvent) => {
        setShowActions(false);
    };

    return (
        <div className="entry_row entry_row--compact" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <EntryRowText href={props.entry.href} title={props.entry.title} />
            <FeedLink href={props.entry.feed.href} title={props.entry.feed.title} />
            <span className="entry_row__date">2 days ago</span>
            <EntryRowActions show={showActions} pin bars/>
        </div>
    )
}
