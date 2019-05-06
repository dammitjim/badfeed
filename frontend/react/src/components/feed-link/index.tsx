import React from "react";

import Props from "./props";

export default (props: Props) => (
    <span className="entry_row__feed">
        <a href={props.href} target="_blank">
            {props.title}
        </a>
    </span>
)
