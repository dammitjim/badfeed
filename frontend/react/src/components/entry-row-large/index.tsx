import React, {useState} from "react";

import EntryRowActions from "../entry-row-actions/index";
import EntryRowMeta from "../entry-row-large-meta/index";
import EntryRowText from "../entry-row-text/index";

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
        <div className="entry_row entry_row--detail" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <div className="entry_row__body">
                <EntryRowText href={props.entry.href} title={props.entry.title} />
                <EntryRowActions show={showActions} pin bars/>
                <span className="entry_row__summary">{props.entry.summary}</span>
                <EntryRowMeta feed={props.entry.feed} datePublished="2 days ago"/>
            </div>
        </div>
    )
}
