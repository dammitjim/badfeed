import * as React from "react";

import Props from "./props";

const entryRowAction = (action: string) => {
    let icon;
    if (action === "Pin") {
        icon = <i className="fas fa-thumbtack"></i>
    }
    else if (action === "Bars") {
        icon = <i className="fas fa-bars"></i>
    }
    return (
        <li className="entry_row__actions__action">
            {icon}
        </li>
    )
};

export default(props: Props) => {
    const actions = [];
    if (props.pin || props.all) {
        actions.push(entryRowAction("Pin"))
    }

    if (props.bars || props.all) {
        actions.push(entryRowAction("Bars"))
    }

    if (props.hide || props.all) {
        actions.push(entryRowAction("Hide"))
    }

    return (
        <ul className="entry_row__actions">
            {actions}
        </ul>
    );
}
