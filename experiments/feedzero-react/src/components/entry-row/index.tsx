import React, {useState} from "react";

import EntryRowActions from "../entry-row-actions/index";
import EntryRowMeta from "../entry-row-meta/index";

import * as Styled from "./styled";
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
        <Styled.Container {...props} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <Styled.Body>
                <Styled.Heading><a href={props.entry.href} target="_blank">{props.entry.title}</a></Styled.Heading>
                <EntryRowActions show={showActions} pin bars/>
                <span>{props.entry.summary}</span>
                <EntryRowMeta feed={props.entry.feed} datePublished="2 days ago"/>
            </Styled.Body>
        </Styled.Container>
    )
}
