import React from "react";

import Props from "./props";
import * as Styled from "./styled";


export default (props: Props) => {
    return (
        <Styled.Container>
            <a href={props.feed.href} target="_blank">
                <Styled.FeedButton>{props.feed.title}</Styled.FeedButton>
            </a>
            <span>{props.datePublished}</span>
        </Styled.Container>
    )
}
