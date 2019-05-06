import React from "react";

import FeedLink from "../feed-link/index";

import Props from "./props";


export default (props: Props) => {
    return (
        <div className="entry_row__body__meta">
            <FeedLink href={props.feed.href} title={props.feed.title} />
            <span className="entry_row__date">{props.datePublished}</span>
        </div>
    )
}
