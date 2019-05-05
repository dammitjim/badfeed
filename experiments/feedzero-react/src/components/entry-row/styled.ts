import styled from "styled-components";

import Props from "./props";

export const Container = styled.div`
    display: flex;
    height: ${(props: Props) => props.detailed ? "100px" : "50px"};
    align-items: center;
    justify-content: center;
    width: 100%;
    border: 1px solid #C2C2C2;
    border-bottom: none;
    padding: 10px;
    position: relative;
    
    ${(props: Props) => props.important && `
        background-color: #FFF9C4;
    `}
    
    &:hover {
        background-color: darken(white, 1%);
    }
    &:last-child,
    &:only-child {
        border-bottom: 1px solid #C2C2C2;
    }
`;

export const Body = styled.div`
    flex-grow: 1;
    display: flex;
    flex-direction: column;
`;

export const Heading = styled.span`
    flex-grow: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    //font-size: $fz--sub;
    font-weight: 600;
`;

export const Summary = styled.span`
`;
