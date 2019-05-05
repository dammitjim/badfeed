import * as React from "react";

import * as Styled from "./styled";
import Props from "./props";

const entryRowAction = (action: string) => {
    return (
        <Styled.Item>
            {action}
        </Styled.Item>
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
        <Styled.List {...props}>
            {actions}
        </Styled.List>
    );
}