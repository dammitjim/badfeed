import React, { useState } from "react";

import Props from "./props";

export default (props: Props) => (
    <span className="entry_row__text">
        <a href={props.href} target="_blank">{props.title}</a>
    </span>
)
